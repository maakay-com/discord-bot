
<p align="center" style="border-radius: 50%">
  <img src="https://user-images.githubusercontent.com/27518021/137136402-800cea06-f7bb-4774-b0fc-fd7860551b5c.jpg">
  <h1 align="center"> Maakay Bot </h1>
</p>

<p>
<img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white"> <img src="https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=green"> <img src="https://img.shields.io/badge/DJANGO-REST-ff1709?style=for-the-badge&logo=django&logoColor=white&color=ff1709&labelColor=gray"> <img src="https://img.shields.io/badge/Discord-7289DA?style=for-the-badge&logo=discord&logoColor=white">
</p>
<h3>Tip friends and create/ host challenges</h3> 

<h4> About Maakay bot</h4>

Maakay-bot is a discord bot made to expand the use TNBC(The new boston coin) around the gaming community by introducing shiny commands specific to gamers. Read below to know more!

Invite the discord bot into your discord server: https://discord.com/api/oauth2/authorize?client_id=893822255816118332&permissions=268435456&scope=bot%20applications.commands

Staging Discord Bot Invite Link: https://discord.com/api/oauth2/authorize?client_id=891676665770541066&permissions=268435456&scope=bot%20applications.commands

#### Contributing
Clone the repo.

Activate the virtual environment.

Install all the requirements using `pip install -r requirements.txt`

Set the required environment variables.
```shell
DJANGO_SETTINGS_MODULE  # config.settings.development
MAAKAY_PAYMENT_ACCOUNT_NUMBER  # TNBC Account number that'll be used to receive payment
SIGNING_KEY  # Signing key of TNBC account that'll be used to transfer TNBC (suggested to use same set of account number and signing key)
BOT_MANAGER_ID  # Discord ID of the user who can use /kill command
MAAKAY_DISCORD_TOKEN  # Discord Token of the bot
SECRET_KEY  # Django Secret Key (Just a random string)
CHECK_TNBC_CONFIRMATION  # Flag to check or not to check confirmations (True/ False)
BANK_IP  # TNBC Bank IP we're connecting to.
```

Create required database and super user.
```shell
python manage.py migrate
python manage.py createsuperuser
```

Run the bot using the command `python maakay-bot.py`.

To run django server, use command `python manage.py runserver`.

Refer `/core` and `/maakay` for API reference.

#### Commands
`/balance`: Check your tnbc balance.

![Balance](https://media.giphy.com/media/uJBfvosVp38Ws2VpDh/giphy.gif)

`/deposit tnbc`: Deposit TNBC into your maakay account.

![Deposit](https://media.giphy.com/media/3SKSF94UXNnJ3fFSoA/giphy.gif)

`/set_withdrawl_address tnbc`: Set your TNBC withdrawal address.

![Set withdrawal adress](https://media.giphy.com/media/NmHoXuxvzwTuTA7mGb/giphy.gif)

`/withdraw tnbc <amount>`: Withdraw TNBC into your withdrawal address.

![Withdraw TNBC](https://media.giphy.com/media/LAXxlgTSH48y2uM0Hz/giphy.gif)

`/transactions tnbc`: List all your deposit and withdraw history.

![Transactions](https://media.giphy.com/media/rEvB7PEPb68QUG5wO5/giphy.gif)

`/profile <user (optional)>`: Check your or other user's maakay gaming profile.

![Profile](https://media.giphy.com/media/oIIXHQjhXKpAQTyMW6/giphy.gif)

`/tip tnbc <user> <amount> <message>`: Tip users TNBC with your beautiful message.

![Tip New](https://media.giphy.com/media/HAWj7zDnDLmTRle2Vj/giphy.gif)

`/tip history`: Check your tip history.

![Tip History](https://media.giphy.com/media/4g5qHsQpYqQUbcr9lF/giphy.gif)

`/challenge new <title> <amount> <contender> <referee>`: Start a new challenge with the contender with referee to reward once challenge is over.

![Challenge new](https://media.giphy.com/media/NEm5Alpm2Lnkt7rWGD/giphy.gif)

`/challenge all`: List all your active challenges.

![Challenge all](https://media.giphy.com/media/NgZgGmNEVauAcvJeTV/giphy.gif)

`/challenge reward <challenge_id> <winner>`: Reward the winner of the challenge.

![Challenge Reward](https://media.giphy.com/media/GtemRFOnKXsZLlRrC7/giphy.gif)

`/challenge history`: List your challenge history.

![Challenge history](https://media.giphy.com/media/o88OqoDzd11gKUiU8N/giphy.gif)

`/host challenge <title> <description> <amount> <url (optional)>`: Host a new challenge with big prizes.

![Host new](https://media.giphy.com/media/iRd2acSIYlV3wWSqls/giphy.gif)

`/host reward <challenge_id> <winner>`: Reward the winner of the challenge.

![Reward Hosted](https://media.giphy.com/media/ez06jglQfHaXxhYDxg/giphy.gif)

`/hosted history`: View your hosted challenge history.

![Hosted History](https://media.giphy.com/media/4vtDhoCI9cBENgdMMH/giphy.gif)

`/hosted all`: View your active hosted challenges.

![Hosted All](https://media.giphy.com/media/JU3S4SQLyuyyQ5NNM1/giphy.gif)
