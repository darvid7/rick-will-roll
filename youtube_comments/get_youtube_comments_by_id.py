## HACKY WRITE TO JSON HERE.
FILENAME = "youtube_comment_data.text"

def write_to_fs(song_name, song_id, comment_list):
  with open(FILENAME, 'a', encoding='utf-8') as fh:
    # Song name, song id, top n comments
    format = '%s, %s, %s\n' % (song_name, song_id, comment_list)
    fh.write(format)
##

#!/usr/bin/python

# Usage example:
# python comments.py --videoid='<video_id>' --text='<text>'

import httplib2
import os
import sys

from apiclient.discovery import build_from_document
from apiclient.errors import HttpError
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import argparser, run_flow


# The CLIENT_SECRETS_FILE variable specifies the name of a file that contains

# the OAuth 2.0 information for this application, including its client_id and
# client_secret. You can acquire an OAuth 2.0 client ID and client secret from
# the {{ Google Cloud Console }} at
# {{ https://cloud.google.com/console }}.
# Please ensure that you have enabled the YouTube Data API for your project.
# For more information about using OAuth2 to access the YouTube Data API, see:
#   https://developers.google.com/youtube/v3/guides/authentication
# For more information about the client_secrets.json file format, see:
#   https://developers.google.com/api-client-library/python/guide/aaa_client_secrets
CLIENT_SECRETS_FILE = "client_secrets.json"

# This OAuth 2.0 access scope allows for full read/write access to the
# authenticated user's account and requires requests to use an SSL connection.
YOUTUBE_READ_WRITE_SSL_SCOPE = "https://www.googleapis.com/auth/youtube.force-ssl"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

# This variable defines a message to display if the CLIENT_SECRETS_FILE is
# missing.
MISSING_CLIENT_SECRETS_MESSAGE = """
WARNING: Please configure OAuth 2.0

To make this sample run you will need to populate the client_secrets.json file
found at:
   %s
with information from the APIs Console
https://console.developers.google.com

For more information about the client_secrets.json file format, please visit:
https://developers.google.com/api-client-library/python/guide/aaa_client_secrets
""" % os.path.abspath(os.path.join(os.path.dirname(__file__),
                                   CLIENT_SECRETS_FILE))

# Authorize the request and store authorization credentials.
def get_authenticated_service(args):
  flow = flow_from_clientsecrets(CLIENT_SECRETS_FILE, scope=YOUTUBE_READ_WRITE_SSL_SCOPE,
    message=MISSING_CLIENT_SECRETS_MESSAGE)

  storage = Storage("%s-oauth2.json" % sys.argv[0])
  credentials = storage.get()

  if credentials is None or credentials.invalid:
    credentials = run_flow(flow, storage, args)

  # Trusted testers can download this discovery document from the developers page
  # and it should be in the same directory with the code.
  with open("youtube-v3-discoverydocument.json", "r", encoding='utf-8') as f:
    doc = f.read()
    return build_from_document(doc, http=credentials.authorize(httplib2.Http()))


# Call the API's commentThreads.list method to list the existing comment threads.
def get_comment_threads(youtube, video_id):
  results = youtube.commentThreads().list(
    part="snippet",
    videoId=video_id,
    textFormat="plainText"
  ).execute()

  text_comments = []

  for item in results["items"]:
    comment = item["snippet"]["topLevelComment"]
    author = comment["snippet"]["authorDisplayName"]
    text = comment["snippet"]["textDisplay"]
    # print("Comment by %s: %s" % (author, text))
    text_comments.append(text)
  return text_comments


# Call the API's comments.list method to list the existing comment replies.
def get_comments(youtube, parent_id):
  print("GET COMMENTS")

  results = youtube.comments().list(
    part="snippet",
    parentId=parent_id,
    textFormat="plainText"
  ).execute()

  text_comments = []
  for item in results["items"]:
    author = item["snippet"]["authorDisplayName"]
    text = item["snippet"]["textDisplay"]
    # TODO: Dump to json?
    print("Comment by %s: %s" % (author, text))
    text_comments.append(text)
  return text


if __name__ == "__main__":


  video_name = "Justin Bieber - What Do You Mean?"
  args = argparser.parse_args()

  youtube = get_authenticated_service(args)

  # Response is a dict.
  response = youtube.search().list(
    q=video_name,
    part="id",
    type="video",
    fields="items/id"
  ).execute()

  # Get first result.
  videos = response['items']
  if len(videos) > 0:
    first_video = videos[0]
    video_id = first_video['id']['videoId']
    print("Video id: %s" % video_id)
    video_comments = get_comment_threads(youtube, video_id)

    write_to_fs(video_name, video_id, video_comments)
    print("Finished song: %s, %s comments" % (video_name, len(video_comments)))
  # # All the available methods are used in sequence just for the sake of an example.
  # try:
  #   video_comment_threads = get_comment_threads(youtube, args.videoid)
  #   parent_id = video_comment_threads[0]["id"]
  #   video_comments = get_comments(youtube, parent_id)
  # except HttpError as e:
  #   print("An HTTP error %d occurred:\n%s" % (e.resp.status, e.content))
  # else:
  #   print("Inserted, listed, updated, moderated, marked and deleted comments.")