import argparse
import urllib
import logging
import os
import errno
import re

DEFAULT_OUTPUT_PATH = os.getcwd() + os.path.sep + 'images' + os.path.sep
DEFAULT_LOG_PATH = os.getcwd() + os.path.sep + 'images_log' + os.path.sep + 'img_downloader.log'


def get_arg_parser():
    """Returns command line argument parser
    :return: parser obj
    """
    parser = argparse.ArgumentParser(description='Image files downloader')
    parser.add_argument('--inputfile', type=str, required=True, help='File path to read image urls')
    parser.add_argument('--outputpath', type=str, default=DEFAULT_OUTPUT_PATH, help='Directory path to store images')
    parser.add_argument('--logfile', type=str, default=DEFAULT_LOG_PATH, help='Directory path for logging messages')
    return parser


def create_directory(directory_path):
    """ Creates directory (if does not exist) using a given path

    :param directory_path:
    :return:
    """
    if not os.path.exists(os.path.dirname(directory_path)):
        try:
            os.makedirs(os.path.dirname(directory_path))
        except OSError as exc:  # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise


def create_directory_with_file(file_path):
    """
    creates directory along with empty file(if does not exist)
    :param file_path:
    :return:
    """
    create_directory(file_path)
    open(file_path, 'a').close()


def sanitize_path(input_path):
    """
    Sanitize invalid path characters ":,|,*" that could be present in url
    :param input_path:
    :return: str
    """
    sanitize_str = re.sub('[:|*]', '', input_path)
    return sanitize_str


def get_path_and_filename_from_url(input_url):
    """
    Returns a tuple (directory path,filename) from a given url
        for e.g http://google.com/signin/abc.png would return (google.com/signin/,abc.png)
    :param input_url:
    :return:
    """
    input_url = input_url.rstrip()
    if input_url:
        start_index = input_url.index('://')
        url_without_http = input_url[start_index + 3:]
        url_path = url_without_http.split("?")
        url_path = url_path[0]
        path_list = url_path.split("/")
        directory_path = os.path.sep.join(path_list[:-1]) + os.path.sep
        filename = path_list[-1]
        return sanitize_path(directory_path), filename
    else:
        return '', ''


def download_image(url, download_file_path):
    """
    Downloads image from a given url to a given path. Returns True if download was successful otherwise False

    :param url:
    :param download_file_path:
    :return:
    """
    try:
        urllib.urlretrieve(url, download_file_path)
        logging.info("successfully downloaded image url: {}".format(url))
        return True
    except IOError, exception:
        logging.error("error downloading image url: {} due to following error:\n{}".format(url, exception))
        return False


def download_images_from_file(input_path, output_path):
    """
    downloads all image files from a given file and stores it in the given output path
    :param input_path:
    :param output_path:
    :return:
    """
    total_urls = 0
    success_count = 0
    with open(input_path) as input_file:
        for line in input_file:
            url = line.rstrip()
            if url:
                url = url if '://' in url else ('http://' + url)
                # create directory from url to avoid overwriting of file in case of duplicate names from different urls
                path, filename = get_path_and_filename_from_url(url)
                download_directory = output_path + os.path.sep + path
                create_directory(download_directory)

                download_path = download_directory + os.path.sep + filename
                status = download_image(url, download_path)
                success_count += 1 if status else 0
                total_urls += 1
    logging.info(
        '{} out of {} image files downloaded successfully to {}'.format(success_count, total_urls, output_path))


def main():
    """
    Execution point of the script that reads url from an input file and stores it to local hard drive. Run:
    python image_downloader.py --inputfile <inputpath> (optional: --outputpath <outputpath> --logpath <logpath>)
    """
    parser = get_arg_parser()
    args = parser.parse_args()

    input_path = args.inputfile
    output_path = args.outputpath
    log_path = args.logfile

    create_directory_with_file(log_path)
    logging.basicConfig(format='%(levelname)s %(asctime)s %(message)s', level=logging.INFO, filename=log_path)
    logging.getLogger().addHandler(logging.StreamHandler())

    logging.info('Urls will be fetched from: {}'.format(input_path))
    logging.info('Images will be stored at: {}'.format(output_path))
    logging.info('Logging at: {}'.format(log_path))

    download_images_from_file(input_path, output_path)


if __name__ == "__main__":
    main()
