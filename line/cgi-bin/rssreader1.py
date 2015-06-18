#!/usr/bin/env python
# coding: utf-8
 
from rssparser import parse_rss
from httphandler import Request, Response, get_htmltemplate
import cgitb; cgitb.enable()
import urllib2
import lxml.html
 
urls = {'主要':'http://news.livedoor.com/topics/rss/top.xml',
'国内':'http://news.livedoor.com/topics/rss/dom.xml',
'海外':'http://news.livedoor.com/topics/rss/int.xml',
'IT 経済':'http://news.livedoor.com/topics/rss/eco.xml',
'芸能':'http://news.livedoor.com/topics/rss/ent.xml',
'スポーツ':'http://news.livedoor.com/topics/rss/spo.xml',
'映画':'http://news.livedoor.com/rss/summary/52.xml',
'グルメ':'http://news.livedoor.com/topics/rss/gourmet.xml',
'女子':'http://news.livedoor.com/topics/rss/love.xml',
'トレンド':'http://news.livedoor.com/topics/rss/trend.xml'}
 
form_body = u"""
<script src="//code.jquery.com/jquery-1.11.3.min.js"></script>
<script type="text/javascript">
function getPage(id,url)  {
	$(id).html('<p>Loading ... </p>');
  	jQuery.ajax({
		url: "/cgi-bin/related.py",
		data:'url='+url,
		type: "POST"
		//success:function(data){alert(data);$(id).html(data['content']);}
	}).success(function(data){
		if (data.length>1) {
			$(id).html('関連リンク<br>'+data);
		} else {
			$(id).html(data);
		}
	}).error(function(XMLHttpRequest,textStatus,errorThrown) {
		alert("error!"+textStatus) ;
	});
}
</script>
<form method="POST" action="/cgi-bin/rssreader1.py">
カテゴリを選んでください
<select name="url" >
<option value=主要>主要</option>
<option value="国内">国内</option> 
<option value="海外">海外</option>    
<option value="IT 経済">IT 経済</option>
<option value="芸能">芸能</option>    
<option value="スポーツ">スポーツ</option>    
<option value="映画">映画</option>  
<option value="グルメ">グルメ</option>
<option value="女子">女子</option>
<option value="トレンド">トレンド</option>        
</select>
<input type="submit"  value="更新する"/>
</form>"""
 
rss_parts = u"""
<h3><a href="%(link)s">%(title)s</a></h3>
<p>%(description)s</p>
"""

sc=u"""
<div id="load%(id)d"></div>
<script type="text/javascript">
getPage("#load%(id)d","%(url)s");
</script>
"""

id=0 
dup=[]
content=u''
req = Request()
if req.form.has_key('url'):
    try:
        rss_list = parse_rss(urls[req.form['url'].value])
        for d in rss_list:
            if not d['link'] in dup:
                content += rss_parts % d
                dup.extend([d['link']])
                #外部リンク
                content+=sc%{'id':id,'url' : d['link']}
                id += 1   
                content += '<hr/>' 
 		 
    except:
        pass
 
res=Response()
body=form_body
body+=content
res.set_body(get_htmltemplate() % body)
print res
