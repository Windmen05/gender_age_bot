# Bot that predicts your age and gender
## Telegram @Age_Sex_bot

### To try
The bot was created using Docker technology and is currently running on AWS server

### Description
The bot is written on the aiogram framework

The pytorch framework was used to train neural networks

#### [Age model](https://www.kaggle.com/windmen/fork-of-notebookef8dca9ec7-2850bf)
the model for predicting age was based on reset 18 because it has a satisfactory accuracy and low flops, which allowed me to train the model on kaggle using the entire [dataset](https://www.kaggle.com/windmen/age-predict) that I had

#### [Gender model](https://www.kaggle.com/windmen/notebook0e2a24ac21)
the resnext50_32x4d model was used as the basis for predicting gender due to the fact that it showed the best result in working with a [dataset](https://www.kaggle.com/windmen/ntechlab2) with human faces

#### DataBase
The results of the bot's prediction are added to the database, which is based on PostgreSQL, which allows the user to see what predictions the bot
gave

:white_check_mark: The user gets a unique id of the image and prediction from the database

:black_square_button: The plans are to make a output in the form of forwarded messages for each image that the bot sent

#### Output to the user
The bot sends the user a ready-made image with the faces marked on it highlighted squares and signed on top of the results of the prediction predicted using cv2, the color of the squares depends on what prediction the model gave to this person

### The architecture of the bot
![Alt-текст](https://github.com/Windmen05/gender_age_bot/blob/master/for_Readme/architecture.png "architecture")

### Sample output
![Alt-текст](https://github.com/Windmen05/gender_age_bot/blob/master/for_Readme/bot_ansver "bot_ansver")
