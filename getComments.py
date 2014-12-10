import requests,csv,argparse,sys,re

def get_reply(activityID, apiKey, writer, video):
    url = 'https://www.googleapis.com/plus/v1/activities/' + activityID + '/comments'
    query_params = {}
    query_params['key'] = apiKey
    query_params['maxResults'] = 500

    r = requests.get(url, params = query_params)
    results = r.json()['items']
    for comment in results:
        row = []
        published = comment['published']
        title = ''
        content = comment['object']['content'].encode('utf8')
        author = comment['actor']['displayName'].encode('utf8')
        reply = 0

        row.extend([video, published, title, content, author.encode('utf8'), reply])
        writer.writerow(row)

def get_comments(url, query_params, writer, video):
    r = requests.get(url, params = query_params)
    results = r.json()['feed']

    comments = result['entry']
    for comment in comments:
        row = []
        published = comment['published']['$t']
        title = comment['title']['$t'].replace(u'\ufeff', '').strip()
        title = title.encode('utf8')
        title = re.sub(r'\n', '', title)

        content = comment['content']['$t'].replace(u'\ufeff', '').strip()
        content = content.encode('utf8')
        content = re.sub(r'\n', '', content)

        author = comment['author'][0]['name']['$t']
        reply = comment['yt$replyCount']['$t']

        row.extend([video, published, title, content, author.encode('utf8'), reply])
        writer.writerow(row)

        if comment['yt$googlePlusUserId'] && reply > 0:
            activityID = comment['id'].split('/')[-1]
            get_reply(activityID,,writer, video)


    if(result['link'][-1]['rel'] == 'next'):
        next = result['link'][-1]['href']
        get_comments(next, '', writer, video)

def main():
    parser = argparse.ArgumentParser(description='getComments. Get all comments from Youtube videos')
    parser.add_argument("-i", "--input", dest="input", help="the path to your .tsv file with videos ID", required=True)
    parser.add_argument("-o", "--output", dest="output", default="output.tsv", help="the output file (.tsv file)")
    options = parser.parse_args()

    data = csv.DictReader(open(options.input, 'rb'), delimiter='\t', skipinitialspace=True)

    site_root = 'https://gdata.youtube.com/feeds/api/videos/'
    site_api = '/comments'

    query_params = {}
    query_params['orderby'] = 'published'
    query_params['alt'] = 'json'
    query_params['max-results'] = 50

    data = list(data)
    total = len(data)

    writer = csv.writer(open(options.output, 'wb'), delimiter='\t', quotechar='"')
    headers = ['id', 'published', 'title', 'content', 'author', 'reply']

    writer.writerow(headers)

    for i, line in enumerate(data):
        video = line['id']
        sys.stdout.write('\x1b[2K\r[' + str(i+1) + '/' + str(total) +'] ' + video)
        sys.stdout.flush()

        site_url = site_root + video + site_api

        get_comments(site_url, query_params, writer, video)
        
        # r = requests.get(site_url, params = query_params)
        # result = r.json()['feed']

        # comments = result['entry']
        # for comment in comments:
        #     row = []
        #     published = comment['published']['$t']
        #     title = comment['title']['$t']
        #     content = comment['content']['$t']
        #     author = comment['author']['name']['$t']
        #     reply = comment['yt$replyCount']['$t']

        #     row.extend([video, published, title, content, author, reply])
        #     writer.writerow(row)

        # if(result['link'][-1]['rel'] == 'next'):
        #     next = result['link'][-1]['href']

            

    sys.stdout.write('\x1b[2K\r')
    sys.stdout.flush()
    sys.exit()

if __name__ == '__main__':
        main()