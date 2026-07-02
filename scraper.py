# -*- coding: utf-8 -*-
import sys
import urllib.parse
import re
import datetime

import xbmcgui
import xbmcplugin
import xbmc
from lib import abema
from lib import Cache

def get_params():
    param_string = sys.argv[2][1:]
    if param_string:
        return dict(urllib.parse.parse_qsl(param_string))
    return {}


params = get_params()
plugin_handle = int(sys.argv[1])
action = params.get('action')

if action == 'find':
    title = params['title']
    year = params.get('year', 'not specified')
    xbmc.log(f'Find movie with title "{title}" from year {year}', xbmc.LOGDEBUG)
    match = re.match(r'^abema:(.*)$', title)
    if match:
        tmp = match.group(1)
        url = tmp.replace(' ', '_')
        param = tmp.split('/')
        season_id = None
        series = param[0]
        if len(param) > 1:
            season_id = param[1].replace(' ', '_')
        info = abema.fetch_series_info(series)
        img = ''
        title = info['title']
        if season_id :
            for season in info['seasons'] :
                if season['id'] != season_id :
                    continue;
                title = season.get('name', title)
                
                img = season['thumbComponent']['urlPrefix']\
                    + '/' + season['thumbComponent']['filename']\
                    + '?' + season['thumbComponent']['query']
        else :
            img = info['thumbComponent']['urlPrefix']\
                + '/' + info['thumbComponent']['filename']\
                + '?' + info['thumbComponent']['query']
        results = [ {'title': title, 'image': img, 'url': url} ]
        
    else:    
        results = abema.find_title(title)
            
    for result in results:
        liz = xbmcgui.ListItem(result['title'], offscreen=True)
        liz.setArt({'thumb': result['image']})
        liz.setProperty('relevance', '1.0')
        xbmcplugin.addDirectoryItem(handle=plugin_handle, url=result['url'], listitem=liz, isFolder=True)
        
elif action == 'getdetails':
    url = params.get('url')
    if url:
        option = url.split('/')
        season_id = None
        series = option[0]
        if len(option) > 1:
            season_id = option[1]
            
        info = abema.fetch_series_info(series)
        title = info['title']
        xbmc.log('Get tv show details callback', xbmc.LOGDEBUG)

        liz = xbmcgui.ListItem(title, offscreen=True)
        tags = liz.getVideoInfoTag()
        tags.setTitle(title)
        tags.setUserRating(5)
        tags.setPlotOutline(info['content'])
        tags.setPlot(info['content'])
        tags.setGenres([info['genre']['name']])
        tags.setEpisodeGuide(url)

        for season in info['seasons'] :
            if season_id and season['id'] != season_id :
                continue;
            tags.addSeason(season['sequence'], season.get('name', 'season'))
    
            img = season['thumbComponent']['urlPrefix']\
                + '/' + season['thumbComponent']['filename']\
                + '?' + season['thumbComponent']['query']

            tags.addAvailableArtwork(img, 'banner', season=season['sequence'])
            tags.addAvailableArtwork(img, 'thumb', season=season['sequence'])

        img = info['thumbPortraitComponent']['urlPrefix']\
            + '/' + info['thumbPortraitComponent']['filename']\
            + '?' + info['thumbPortraitComponent']['query']

        tags.addAvailableArtwork(img, 'poster')
        tags.addAvailableArtwork(img, 'fanart')
            
        liz.setAvailableFanart([{'image': img}])
        xbmcplugin.setResolvedUrl(handle=plugin_handle, succeeded=True, listitem=liz)

elif action == 'getepisodelist':
    url = params.get('url')
    option = url.split('/')
    season_id = None
    series = option[0]
    if len(option) > 1:
        season_id = option[1]

    groups = Cache().get_or_download_series(series)
    for group in groups :
        season_seq = group['sequence']
        if season_id and group['id'] != season_id :
            continue;

        if group['episodeGroups'] :
            for eg in group['episodeGroups'] :
                episodes = Cache().get_or_download_list(group['id'], eg['id'])
                for ep in episodes:
                    liz = xbmcgui.ListItem(ep['episode']['title'], offscreen=True)
                    tags = liz.getVideoInfoTag()
                    tags.setTitle(ep['episode']['title'])
                    season_seq = int(re.match(r'.*s(\d+)_p', ep['id']).group(1))
                    tags.setSeason(season_seq)
                    tags.setEpisode(ep['episode']['number'])
                    img = ep['thumbComponent']['urlPrefix']\
                        + '/' + ep['thumbComponent']['filename']\
                        + '?' + ep['thumbComponent']['query']

                    tags.setYear(ep['video']['releaseYear'])
                    tags.addAvailableArtwork(img, 'banner')
                    tags.addAvailableArtwork(img, 'thumb')
                    ep_url = ep['id']
                    liz.setAvailableFanart([{'image': img}])
                    xbmcplugin.addDirectoryItem(handle=plugin_handle, url=ep_url, listitem=liz, isFolder=False)
        else :
            episodes = Cache().get_or_download_list(group['season'], None)
            for ep in episodes:
                liz = xbmcgui.ListItem(ep['episode']['title'], offscreen=True)
                tags = liz.getVideoInfoTag()
                tags.setTitle(ep['episode']['title'])
                tags.setSeason(ep['season']['sequence'])
                tags.setEpisode(ep['episode']['number'])
                video_id = ep['id']
                img = f'https://image.p-c2-x.abema-tv.com/image/programs/{video_id}/thumb001.png'

                tags.addAvailableArtwork(img, 'banner')
                tags.addAvailableArtwork(img, 'thumb')
                ep_url = ep['id']
                liz.setAvailableFanart([{'image': img}])
                xbmcplugin.addDirectoryItem(handle=plugin_handle, url=ep_url, listitem=liz, isFolder=False)

elif action == 'getepisodedetails':
    url = params['url']
    episode = url

    info = abema.fetch_episode(episode)
    xbmc.log('Get episode 1 details callback', xbmc.LOGDEBUG)
    liz = xbmcgui.ListItem(info['episode']['title'], offscreen=True)
    tags = liz.getVideoInfoTag()
    tags.setTitle(info['episode']['title'])
    tags.setSeason(info['season']['sequence'])
    tags.setEpisode(info['episode']['number'])
    tags.setPlotOutline(info['episode']['content'])
    tags.setPlot(info['episode']['content'])
    tags.setDuration(info['info']['duration'])
    dt = datetime.datetime.fromtimestamp(info['data']['broadcastDate'])
    tags.setFirstAired(dt.strftime('%Y-%m-%d'))
    genres = []
    genres.append(info['genre']['name'])
    if 'subGenres' in info['genre'].keys():
        for genre in info['genre']['subGenres']:
            genres.append(genre['name'])
    tags.setGenres(genres)
    tags.setUniqueIDs({'abema': episode}, defaultuniqueid='abema')
    tags.addSeason(info['season']['sequence'], info['season']['name'])
    #https://image.p-c2-x.abema-tv.com/image/programs/19-171_s1_p1/thumb002.png?height=143&quality=75&version=1765276796&width=256
    if 'providedInfo' in info.keys():
        if 'sceneThumbImgs' in info['providedInfo'].keys():
            for item in info['providedInfo']['sceneThumbImgs']:
                img = f'https://image.p-c2-x.abema-tv.com/image/programs/{episode}/{item}.png'
                tags.addAvailableArtwork(img, 'banner')
                tags.addAvailableArtwork(img, 'thumb')
        fname = info['providedInfo']['thumbImg']
        img = f'https://image.p-c2-x.abema-tv.com/image/programs/{episode}/{fname}.png'
        tags.addAvailableArtwork(img, 'banner')
        tags.addAvailableArtwork(img, 'thumb')
                    
    xbmcplugin.setResolvedUrl(handle=plugin_handle, succeeded=True, listitem=liz)


elif action is not None:
    xbmc.log(f'Action "{action}" not implemented', xbmc.LOGDEBUG)

xbmcplugin.endOfDirectory(plugin_handle)
