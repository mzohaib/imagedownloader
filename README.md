# image downloader
The script downloads all images from the input file path and stores it to the given output path. Additionally, it generates logs on console as well as in a given log file path.
<br/><br/>
Run Python script using the following command on shell: <br/>
<code>
python image_downloader.py --inputfile <inputfile> INPUTFILE [--outputpath OUTPUTPATH] [--logfile LOGFILE]
</code>

### Deployment (One Time Setup on each machine)
1. Configure Web Server(for e.g. Apache) to serve the desired folder available via http
2. Copy the script and cron it for the desired frequency. For example to run every 5 minutes execute on shell:<br/>
<code>
*/5 * * * * /path/to/image_downloader.py
</code>
