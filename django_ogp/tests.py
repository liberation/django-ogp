from django.test import TestCase
from django.db import models
from django.template import Template, Context

class TestModel(models.Model):
    pass


class OGPTestModel(TestModel):
    ogp_enabled = True
    
    def ogp_title(self):
        return 'The Rock'
    
    def ogp_type(self):
        return 'movie'
    
    def ogp_url(self):
        return 'http://www.imdb.com/title/tt0117500/'
    
    def ogp_image(self):
        return 'http://ia.media-imdb.com/images/rock.jpg'


class OGPCompleteTestModel(OGPTestModel):
    def ogp_latitude(self):
        return 37.416343

    def ogp_longitude(self):
        return -122.153013

    def ogp_video_width(self):
        return 1024

    def ogp_video_height(self):
        return 800


class OGPTest(TestCase):
    def test_ogp_rendering(self):
        """
        Tests that an instance can render OGP infos.
        """        
        self.assertEqual(u'xmlns:og="http://ogp.me/ns#"', 
                        Template("{% load ogp_tags %}{% ogp_namespace %}").render(Context()))
        self.assertEqual(u'', 
                        Template("{% load ogp_tags %}{% render_ogp item %}").render(Context({'item': TestModel()})))
        self.assertEqual(u'<meta property="og:url" content="http://www.imdb.com/title/tt0117500/" /><meta property="og:image" content="http://ia.media-imdb.com/images/rock.jpg" /><meta property="og:type" content="movie" /><meta property="og:title" content="The Rock" />', 
                        Template("{% load ogp_tags %}{% render_ogp item %}").render(Context({'item': OGPTestModel()})))
        self.assertEqual(u'<meta property="og:title" content="The Rock" /><meta property="og:url" content="http://www.imdb.com/title/tt0117500/" /><meta property="og:image" content="http://ia.media-imdb.com/images/rock.jpg" /><meta property="og:longitude" content="-122.153013" /><meta property="og:video:height" content="800" /><meta property="og:video:width" content="1024" /><meta property="og:latitude" content="37.416343" /><meta property="og:type" content="movie" />', 
                        Template("{% load ogp_tags %}{% render_ogp item %}").render(Context({'item': OGPCompleteTestModel()})))
