from pixivpy3 import *

import re, os

save_image_path = './images/'  # this config is global!
if not os.path.exists(save_image_path):
    os.makedirs(save_image_path)

api = AppPixivAPI()
api.login("your_username", "your_password")


def find_suffix(filename:'str'):
    '''
    :param filename: 'https://i.pximg.net/img-original/img/2020/08/15/22/49/08/83705920_p0.png'
    :return: '.png'
    '''
    return re.search(r'\.[^.\\/:*?"<>|\r\n]+$', filename).group()


def file_already_exists(filename):
    return os.path.exists(os.path.join(save_image_path,filename))


def gen_illust_filenames_and_urls(illust):
    '''
    :param illust: api.search_illust('some_tag')[0]
    :return: [('13123112_2_sanity_level_2.png', 'the_url'), ...]
    '''
    if illust['meta_pages'] and not illust['meta_single_page']:
        l = len(illust['meta_pages'])
        return [(f'''{illust['id']}_{i}_sanity_{illust['sanity_level']}{find_suffix(illust['meta_pages'][i]['image_urls']['original'])}''', illust['meta_pages'][i]['image_urls']['original']) for i in range(l)]
    elif illust['meta_single_page']:
        return [(f'''{illust['id']}_{0}_sanity_{illust['sanity_level']}{find_suffix(illust['meta_single_page']['original_image_url'])}''', illust['meta_single_page']['original_image_url'])]
    else:
        raise ValueError('Contact developers to debug gen_illust_filenames')

def download_increment(illust):
    pairs = gen_illust_filenames_and_urls(illust)
    for pair in pairs:
        filename, url = pair[0], pair[1]
        if file_already_exists(filename):
            pass  # do nothing!
        else:
            api.download(url,path=save_image_path, name=filename)
    return

# json_result = api.search_illust('クトリ・ノタ・セニオリス', search_target='exact_match_for_tags')
# json_result = api.search_illust('終末なにしてますか?もう一度だけ、会えますか?', search_target='exact_match_for_tags')
while 1:
    json_result = api.search_illust('終末なにしてますか?忙しいですか?救ってもらっていいですか?', search_target='exact_match_for_tags')
    for illust in json_result['illusts']:
        download_increment(illust)
    try:
        next_qs = api.parse_qs(json_result.next_url)
    except:
        break
    json_result = api.illust_related(**next_qs)
