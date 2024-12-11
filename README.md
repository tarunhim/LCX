Website Sharing - 
                This automation script interacts with various external sources, including CNN's RSS feed, a caption generation API, and an image/video generation API. It also utilizes SQLite, a popular database, to persist the processed data.

                The script begins by setting up the SQLite database for storing article details, captions, media links, and URLs. It then fetches new articles from CNN's RSS feed, checks if they have been processed previously based on their unique URLs, and proceeds to process only the new ones.

                Once i have the list of new articles, i am iterating over that and creating caption and generating images and entering the data in sqlite db,

                Now about the generated caption and image part, i didn't had enough time to go through and get api keys of open ai or other tools to integrate in my code hence i have decided to simulate those functionality for now, so i have written funtions simulating those two things but in reality they are returning normal data

                now in the last part of the assignment, it need to be rendered on a web page, hence i have added a flask api as well to list down all data which i am saving in sqlite.

                