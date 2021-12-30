# Re-prezent

A simple web application for collecting Facebook posts from public pages and viewing the images they contain according to the objects they depict. The tool uses the facebook-scraper python package developed and maintained by @neon-ninja and @kevinzg, the django web framework, and can be connected to any image recognition service available (I use GOOGLE's vision).
<br><br>
As a research tool, the application is meant to allow researchers to see social media images in groups to help reconceptualise the use of objects by public actors. The tool was originally created to study how politicians use images of different objects in their public communcation strategies, but could be applied to other types of public actors.
<br>The code is far from done, will update continually.

<hr>

# Project use

As a research tool a website like this can be super informative, however, due to different privacy laws in different countries publicising it may require permission. My version took parliamentarians in Hungary as a list of public figures, and although the running website is private, I've included below some images to demonstrate the data I got and how the website itself would look like.

#### Ten image tags with highest counts recorded between 06/2021 and 09/2021.<br>
![alt text](https://github.com/everybitmihaly/Re-prezent/blob/master/top_10_tags.png?raw=true)

#### Collage of random images tagged as 'Podium'.<br>
![alt text](https://github.com/everybitmihaly/Re-prezent/blob/master/podium_collage.png?raw=true)

#### Network of top 65 tags ordered by edge connectivity.<br>
![alt text](https://github.com/everybitmihaly/Re-prezent/blob/master/tag_network.png?raw=true)

#### Image library search results for the tag 'Airplane'.<br>
![alt text](https://github.com/everybitmihaly/Re-prezent/blob/master/search_result.png?raw=true)
