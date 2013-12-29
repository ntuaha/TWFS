import os
import sys
import psycopg2
from types import *




$normal_message = 'hello';
$api = '688430041191592'; 
$api_secret = '6bb097ca9fe10f1bca0c1c320232eba2';
$callback_website = urlencode('https://github.com/ntuaha/TWFS/');
$picture_url_tick = 'http://www.iconarchive.com/icons/pixelmixer/basic/64/tick-icon.png';
$caption='la la';
$facebook_id = '100000185149998';

/usr/local/bin/curl -F grant_type=client_credentials -F client_id=688430041191592 -F client_secret=6bb097ca9fe10f1bca0c1c320232eba2 -k https://graph.facebook.com/oauth/access_token

https://graph.facebook.com/oauth/authorize?
    client_id=688430041191592&
    redirect_uri=pages/Ahas-Robot-Community/437575193035602&
    scope=user_photos,user_videos,publish_stream


//GET access_token
exec(sprintf("/usr/local/bin/curl -F grant_type=client_credentials -F client_id=%s -F client_secret=%s -k https://graph.facebook.com/oauth/access_token",$api,$api_secret),$result);
list($key,$access_token)= explode('=',$result[0]);

688430041191592|1apOpKzaTmbqC6AIjvSSlJF-4Jo



//Post Message
exec(sprintf("/usr/local/bin/curl -F 'access_token=%s' -F 'message=%s' -F 'name=Working' -F 'picture=%s' -F 'caption=%s' -k https://graph.facebook.com/%s/feed",
            $access_token,$normal_message,$picture_url_tick,$caption,$facebook_id),$result);



curl -F 'access_token=688430041191592|1apOpKzaTmbqC6AIjvSSlJF-4Jo' -F 'message=hello' -F 'name=Working' -F 'picture=http://www.iconarchive.com/icons/pixelmixer/basic/64/tick-icon.png' -F 'caption=GG' -k https://graph.facebook.com/100000185149998/feed
