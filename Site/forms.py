import json
import urllib
from random import randint
from urllib.request import urlopen
import ssl
from django import forms
from django.contrib.auth.models import User
from Site.models import Photo, Followers, Owner, Post

ssl._create_default_https_context = ssl._create_unverified_context


class Ajax(forms.Form):
    args = []
    user = []

    def __init__(self, *args, **kwargs):

        self.args = args
        if len(args) > 1:
            self.user = args[1]
            if self.user.id == None:
                self.user = "NL"

    def error(self, message):
        return json.dumps({"Status": "Error", "Message": message}, ensure_ascii=False)

    def success(self, message):
        return json.dumps({"Status": "Success", "Message": message}, ensure_ascii=False)

    def items(self, json):
        return json

    def output(self):
        return self.validate()


class AjaxSavePhoto(Ajax):
    def validate(self):
        try:
            self.url = self.args[0]["url"]
            self.baseurl = self.args[0]["baseurl"]
            self.caption = self.args[0]["caption"]
        except Exception as e:
            return self.error("Malformed request, did not process.")

        if self.user == "NL":
            return self.error("Unauthorised request.")

        if len(self.caption) > 140:
            return self.error("Caption must be 140 characters.")

        if self.url[0:20] != "https://ucarecdn.com" or self.baseurl[0:20] != "https://ucarecdn.com":
            return self.error("Invalid image URL")

        result = urlopen(self.baseurl + "-/preview/-/main_colors/3/")
        data = result.read()
        data = json.loads(data.decode('utf-8'))

        main_colour = ""
        if data["main_colors"]:
            # main_colour = data["main_colors"][randint(0, 2)]
            for colour in data["main_colors"][randint(0, 2)]:
                main_colour = main_colour + str(colour) + ","
            main_colour = main_colour[:-1]

        result = urllib.request.urlopen(self.baseurl + "detect_faces/")
        data = result.read()
        data = json.loads(data.decode('utf-8'))

        tag_count = 0
        p = Photo(url=self.url, baseurl=self.baseurl, owner=self.user.username, caption=self.caption,
                  main_colour=main_colour)
        p.save()
        p.save()

        return self.success("Image Uploaded")


class AjaxPhotoFeed(Ajax):
    def validate(self):
        try:
            self.start = self.args[0]["start"]
        except Exception as e:
            return self.error("Malformed request, did not process.")
        out = []
        followerslist = [self.user.username]
        profilepics = {}

        for follower in Followers.objects.filter(follower=self.user.username):
            followerslist.append(follower.user)

        for item in Photo.objects.filter(owner__in=followerslist).order_by('-date_uploaded')[
                    int(self.start):int(self.start) + 3]:

            out.append(
                {"PostID": item.id, "URL": item.url, "Caption": item.caption, "Owner": item.owner,
                 "DateUploaded": item.date_uploaded.strftime("%Y-%m-%d %H:%M:%S"),
                 "MainColour": item.main_colour})

        return self.items(json.dumps(out))
