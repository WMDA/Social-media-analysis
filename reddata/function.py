import yaml
import argparse


def load_config(config_file = "config.yaml"):
    '''
        Loads config file

        Parameters:
        ----------
        config file

        Returns
        -------
        config file content
    '''

    config_yml = open(config_file)
    config = yaml.load(config_yml, yaml.SafeLoader)
    return config

def get_arguments():
    '''
        Defines command line arguments

        Parameters:
        ----------
        None

        Returns
        -------
        Optional and Required command line arguments
    '''
    parse = argparse.ArgumentParser(usage='pipeline [-t] [-c] [<options>] \n or: pipeline [-config] [<options>]')
    parse.add_argument("-t", "--topics", dest='topics', nargs='*', help='Topics that praw will search reddit for. Required if -config not used. For use multiple word arguments use " ". ')
    parse.add_argument("-c","--comments", dest='comments', help='Selects number of comments for praw to limit to. Required if -config not used.')
    parse.add_argument("-config",help="Uses config.yaml file instead of providing options, doesn't take any arguments but needs config.yaml file (provided with package).",action="store_true")
    parse.add_argument("-csv", help="Saves output to CSV, needs a directory to save csv to.")
    parse.add_argument("-n","--name", dest='name', help="Gives the file a name, if this option is not used in conjunction with -csv then file will be called reddit_database.")
    parse.add_argument("-gbq","--bigquery",dest="gbq",help="Saves results to google bigquery reddit_table. Needs project id (found on google cloud platform), reddit_table also needs name so flag -n must be used.")
    parse.add_argument("-s","--sort", dest="sort", help="Tells pipeline to sort for comments based on attribute. If this argument isn't used then the default is new. Needs one of the following arguments: controversial, gilded, hot, rising, top")
    options= parse.parse_args()
    if options.sort:
        sort_list =["controversal", 'gilded', 'hot','rising', 'top']
        if options.sort not in sort_list:
            parse.error("Unknown sort option given. Use -h for support")
    if options.gbq and not options.name:
        parse.error(">> -gbq table needs a name, use -n to give name to reddit_table. Use -h for more info or go to https://github.com/WMDA/social-media-analysis")
    elif options.config:
        config = load_config()
        options.topics=config["topics"]
        options.comments= config["comments"]
        return options
    elif not options.topics or not options.comments:
        parse.error(">> Needs topic and number of comment. Use -t and put topics and -c to put number of comments or use -config. Use -h for more information or go to https://github.com/WMDA/social-media-analysis.")
    else:
        return options


def print_output(topic,comments,*args):
    '''
            Prints to console topics being serached for, comments limited to and how comments are sorted.

            Parameters:
            ----------
            topics being search for, comments limited to and *args

            Returns
            -------
            Prints to console topics being serached for, comments limited to and how comments are sorted.
    '''

    print('\n','Searching reddit for','\n',topic)
    print('\n','Limiting comments to','\n', comments)
    if args:
        print('\n','Sorting comments based on: %s' %args)
    else:
        print('\n',"Sorting comments based on: new")
