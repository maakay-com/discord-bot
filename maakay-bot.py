import os
from discord.colour import Color
from discord.errors import Forbidden
import django
import discord
from asgiref.sync import sync_to_async
from discord_slash import SlashCommand
from discord_slash.context import ComponentContext
from discord_slash.utils.manage_components import create_button, create_actionrow
from discord_slash.model import ButtonStyle
from discord.ext import commands
from discord_slash.utils.manage_commands import create_option, create_choice

# Django Setup on bot
DJANGO_DIRECTORY = os.getcwd()
os.environ.setdefault("DJANGO_SETTINGS_MODULE", os.environ["DJANGO_SETTINGS_MODULE"])
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
django.setup()

from django.conf import settings
from core.utils.scan_chain import match_transaction, check_confirmation, scan_chain
from maakay.models.challenge import Challenge
from core.models.user import User
from core.models.guild import Guild

# Environment Variables
TOKEN = os.environ['MAAKAY_DISCORD_TOKEN']
TOURNAMENT_FEE_MULTIPLICATION = (100 - settings.TOURNAMENT_FEE) / 100

# Initialize the Slash commands
bot = commands.Bot(command_prefix=">")
bot.remove_command('help')
slash = SlashCommand(bot, sync_commands=True)

gifs = {
    "new_challenge": "https://media.giphy.com/media/NEm5Alpm2Lnkt7rWGD/giphy.gif",
    "reward_challenge": "https://media.giphy.com/media/GtemRFOnKXsZLlRrC7/giphy.gif",
    "challenge_all": "https://media.giphy.com/media/NgZgGmNEVauAcvJeTV/giphy.gif",
    "challenge_history": "https://media.giphy.com/media/o88OqoDzd11gKUiU8N/giphy.gif",
    "new_hosted_challenge": "https://media.giphy.com/media/iRd2acSIYlV3wWSqls/giphy.gif",
    "reward_hosted_challenge": "https://media.giphy.com/media/ez06jglQfHaXxhYDxg/giphy.gif",
    "hosted_all": "https://media.giphy.com/media/JU3S4SQLyuyyQ5NNM1/giphy.gif",
    "hosted_history": "https://media.giphy.com/media/4vtDhoCI9cBENgdMMH/giphy.gif",
    "set_withdraw_address": "https://media.giphy.com/media/NmHoXuxvzwTuTA7mGb/giphy.gif",
    "deposit": "https://media.giphy.com/media/3SKSF94UXNnJ3fFSoA/giphy.gif",
    "balance": "https://media.giphy.com/media/uJBfvosVp38Ws2VpDh/giphy.gif",
    "tip_new": "https://media.giphy.com/media/HAWj7zDnDLmTRle2Vj/giphy.gif",
    "tip_history": "https://media.giphy.com/media/4g5qHsQpYqQUbcr9lF/giphy.gif",
    "withdraw": "https://media.giphy.com/media/LAXxlgTSH48y2uM0Hz/giphy.gif",
    "transactions": "https://media.giphy.com/media/rEvB7PEPb68QUG5wO5/giphy.gif",
    "profile": "https://media.giphy.com/media/oIIXHQjhXKpAQTyMW6/giphy.gif"
}

@bot.event
async def on_ready():
    print("------------------------------------")
    print("maakay Bot Running:")
    print("------------------------------------")
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name="/help"))

@bot.event
async def on_guild_join(guild):
    
    guild_obj, created = Guild.objects.get_or_create(guild_id=str(guild.id))

    try:
        role = await guild.create_role(name="Maakay Bot Admin", hoist=True, reason="Role for the Maakay bot admin", colour=discord.Colour.red())
        guild_obj.manager_role_id = role.id
        guild_obj.has_permissions = True
        guild_obj.save()

    except Forbidden:

        guild_obj.has_permissions = False
        guild_obj.save()

        print("Permission error smh")

@slash.subcommand(base="help", name="all", description="List of Commands!!")
async def help_all(ctx):
    
    embed = discord.Embed(title="Commands", color=Color.orange(), description="Use `/help <category>` for category specific commands")
    embed.set_footer(text="Fields with * are required!!")
    embed.set_thumbnail(url=bot.user.avatar_url)
    embed.add_field(name="/balance", value="Check your balance.", inline=False)
    embed.add_field(name="/deposit tnbc", value="Deposit TNBC into your maakay account.", inline=False)
    embed.add_field(name="/set_withdrawl_address tnbc `<your withdrawl address>*`", value="Set a new withdrawl address.", inline=False)
    embed.add_field(name="/withdraw tnbc `<amount>*`", value="Withdraw TNBC into your account.", inline=False)
    embed.add_field(name="/transactions tnbc", value="Check Transaction History!!", inline=False)
    embed.add_field(name="/profile `<user you want to check profile of>*`", value="Check profile of an user.", inline=False)
    embed.add_field(name="/tip tnbc `<amount>*` `<user you want to tip>*` `<title for the tip>*`", value="Tip another user!!", inline=False)
    embed.add_field(name="/tip history", value="View tip history!!", inline=False)
    embed.add_field(name="/challenge new `<title of the challenge>*` `<amount>*` `<contender>*` `<referee>*`", value="Create a new challenge!!", inline=False)
    embed.add_field(name="/challenge reward `<challenge id>*` `<challenge winner>*`", value="Reward the challenge winner!", inline=False)
    embed.add_field(name="/challenge history", value="Show the history of challenges in which the user participated!!", inline=False)
    embed.add_field(name="/challenge all", value="List all the active challenges!!", inline=False)
    embed.add_field(name="/challenge cancel `<challenge id>*`", value="Cancel a challenge (only if referee hasn't accepted it yet)", inline=False)
    embed.add_field(name="/host challenge `<title>*` `<description>*` `<amount>*` `<url for more info>*`", value="Host a new challenge!!", inline=False)
    embed.add_field(name="/host reward `<challenge id>*` `<challenge winner>*`", value="Reward the challenge winner!!", inline=False)
    embed.add_field(name="/hosted history", value="List of hosted challenges you participated in!!", inline=False)
    embed.add_field(name="/hosted all", value="List of active hosted challenges!!", inline=False)
    await ctx.send(embed=embed, hidden=True)


@slash.subcommand(base="help", name="general", description="List of Commands from General Category")
async def help_general(ctx):
    embed = discord.Embed(title="General Commands", color=Color.orange())
    embed.set_footer(text="Fields with * are required!!")
    embed.set_thumbnail(url=bot.user.avatar_url)

    embed.add_field(name="/balance", value="Check your balance.", inline=False)
    embed.add_field(name="/deposit tnbc", value="Deposit TNBC into your maakay account.", inline=False)
    embed.add_field(name="/set_withdrawl_address tnbc `<your withdrawl address>*`", value="Set a new withdrawl address.", inline=False)
    embed.add_field(name="/withdraw tnbc `<amount>*`", value="Withdraw TNBC into your account.", inline=False)
    embed.add_field(name="/transactions tnbc", value="Check Transaction History!!", inline=False)
    embed.add_field(name="/profile `<user you want to check profile of>*`", value="Check profile of an user.", inline=False)

    await ctx.send(embed=embed, hidden=True)


@slash.subcommand(base="help", name="tip", description="List of Commands from Tip Category")
async def help_tip(ctx):
    embed = discord.Embed(title="Tip Commands", color=Color.orange())
    embed.set_footer(text="Fields with * are required!!")
    embed.set_thumbnail(url=bot.user.avatar_url)

    embed.add_field(name="/tip tnbc `<amount>*` `<user you want to tip>*` `<title for the tip>*`", value="Tip another user!!", inline=False)
    embed.add_field(name="/tip history", value="View tip history!!", inline=False)

    await ctx.send(embed=embed, hidden=True)


@slash.subcommand(base="help", name="challenge", description="List of Commands from Challenge Category")
async def help_challenge(ctx):
    embed = discord.Embed(title="Challenge Commands", color=Color.orange())
    embed.set_footer(text="Fields with * are required!!")
    embed.set_thumbnail(url=bot.user.avatar_url)

    embed.add_field(name="/challenge new `<title of the challenge>*` `<amount>*` `<contender>*` `<referee>*`", value="Create a new challenge!!", inline=False)
    embed.add_field(name="/challenge reward `<challenge id>*` `<challenge winner>*`", value="Reward the challenge winner!", inline=False)
    embed.add_field(name="/challenge history", value="Show the history of challenges in which the user participated!!", inline=False)
    embed.add_field(name="/challenge all", value="List all the active challenges!!", inline=False)
    embed.add_field(name="/challenge cancel `<challenge id>*`", value="Cancel a challenge (only if referee hasn't accepted it yet)", inline=False)

    await ctx.send(embed=embed, hidden=True)

@slash.subcommand(base="help", name="hosted_challenge", description="List of Commands from Hosted Challenge Category")
async def help_hosted_challenge(ctx):
    embed = discord.Embed(title="Hosted Challenge Commands", color=Color.orange())
    embed.set_footer(text="Fields with * are required!!")
    embed.set_thumbnail(url=bot.user.avatar_url)

    embed.add_field(name="/host challenge `<title>*` `<description>*` `<amount>*` `<url for more info>*`", value="Host a new challenge!!", inline=False)
    embed.add_field(name="/host reward `<challenge id>*` `<challenge winner>*`", value="Reward the challenge winner!!", inline=False)
    embed.add_field(name="/hosted history", value="List of hosted challenges you participated in!!", inline=False)
    embed.add_field(name="/hosted all", value="List of active hosted challenges!!", inline=False)

    await ctx.send(embed=embed, hidden=True)

@slash.subcommand(base="help", name="gif", description="Show gif for usage of a  specific command", options=[
    create_option(name="command_name", description="Command which you wanna see gif of", option_type=3, required=True, choices=[
        create_choice(name="Create Challenge", value="new_challenge"),
        create_choice(name="Reward Challenge", value="reward_challenge"),
        create_choice(name="Challenge History", value="challenge_history"),
        create_choice(name="Active Challenges", value="challenge_all"),
        create_choice(name="Deposit TNBC", value="deposit"),
        create_choice(name="Withdraw TNBC", value="withdraw"),
        create_choice(name="Check Balance", value="balance"),
        create_choice(name="Transactions History", value="transactions"),
        create_choice(name="Check user profile", value="profile"),
        create_choice(name="Tip an user", value="tip_new"),
        create_choice(name="Check tip history", value="tip_history"),
        create_choice(name="Host a challenge", value="new_hosted_challenge"),
        create_choice(name="Reward a hosted challenge", value="reward_hosted_challenge"),
        create_choice(name="Hosted challenge history", value="hosted_history"),
        create_choice(name="Active Hosted Challenges", value="hosted_all"),
        create_choice(name="Set withdraw address", value="set_withdraw_address"),
        ])
    ])

async def help_gif(ctx, command_name):
    await ctx.send(gifs[command_name], hidden=True)


for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')


@bot.event
async def on_component(ctx: ComponentContext):

    button = ctx.custom_id.split('_')

    button_type = button[0]

    if button_type == "challenge":

        embed = discord.Embed()

        obj, created = await sync_to_async(User.objects.get_or_create)(discord_id=str(ctx.author.id))

        challenge_uuid = button[2]

        if Challenge.objects.filter(uuid=challenge_uuid, status=Challenge.NEW).exists():

            button_action = button[1]

            challenge = await sync_to_async(Challenge.objects.get)(uuid=challenge_uuid)

            challenger = await bot.fetch_user(int(challenge.challenger.discord_id))
            contender = await bot.fetch_user(int(challenge.contender.discord_id))
            referee = await bot.fetch_user(int(challenge.referee.discord_id))

            if challenge.contender == obj:
                if challenge.contender_status == Challenge.PENDING:
                    if button_action == "accept":
                        if obj.get_available_balance() >= challenge.amount:
                            if challenge.referee_status == Challenge.ACCEPTED:
                                challenge.status = Challenge.ONGOING
                            challenge.contender_status = Challenge.ACCEPTED
                            challenge.contender.locked += challenge.amount
                            challenge.contender.save()
                            challenge.save()
                            embed.add_field(name="Accepted", value=f"Challenge accepted by contender {contender.mention}", inline=False)
                            embed.add_field(name="Title", value=challenge.title)
                            embed.add_field(name="Amount (TNBC)", value=f"**{challenge.get_decimal_amount()}**")
                            embed.add_field(name="Challenger", value=f"{challenger.mention}")
                            embed.add_field(name="Contender", value=f"{contender.mention}")
                            embed.add_field(name="Referee", value=f"{referee.mention}")
                            embed.add_field(name="Status", value=challenge.status)
                            await ctx.send(f"{challenger.mention} {referee.mention}", embed=embed)
                        else:
                            embed.add_field(name="Error!", value=f"You only have {obj.get_decimal_available_balance()} TNBC out of {challenge.get_decimal_amount()} TNBC.\nPlease use `/user deposit` command to deposit TNBC.")
                            await ctx.send(embed=embed, hidden=True)
                    else:
                        challenge.contender_status = Challenge.REJECTED
                        challenge.status = Challenge.CANCELLED
                        challenge.save()
                        challenge.challenger.locked -= challenge.amount
                        challenge.challenger.save()
                        embed.add_field(name="Rejected", value=f"Challenge rejected by contender {contender.mention}")
                        await ctx.send(f"{challenger.mention} {referee.mention}", embed=embed)
                else:
                    embed.add_field(name="Sorry", value=f"You've already accepted/ rejected *{challenge.title}*")
                    await ctx.send(embed=embed, hidden=True)
            elif challenge.referee == obj:
                if challenge.referee_status == Challenge.PENDING:
                    if button_action == "accept":
                        if challenge.contender_status == Challenge.ACCEPTED:
                            challenge.status = Challenge.ONGOING
                            challenge.contender.locked += challenge.amount
                            challenge.contender.save()
                        challenge.referee_status = Challenge.ACCEPTED
                        challenge.save()
                        embed.add_field(name="Accepted", value=f"Challenge accepted by referee {referee.mention}", inline=False)
                        embed.add_field(name="Title", value=challenge.title)
                        embed.add_field(name="Amount (TNBC)", value=f"**{challenge.get_decimal_amount()}**")
                        embed.add_field(name="Challenger", value=f"{challenger.mention}")
                        embed.add_field(name="Contender", value=f"{contender.mention}")
                        embed.add_field(name="Referee", value=f"{referee.mention}")
                        embed.add_field(name="Status", value=challenge.status)
                        await ctx.send(f"{challenger.mention} {contender.mention}", embed=embed)
                    else:
                        challenge.referee_status = Challenge.REJECTED
                        challenge.status = Challenge.CANCELLED
                        challenge.save()
                        challenge.challenger.locked -= challenge.amount
                        challenge.challenger.save()
                        embed.add_field(name="Rejected", value=f"Challenge rejected by referee {referee.mention}")
                        await ctx.send(f"{challenger.mention} {contender.mention}", embed=embed)
                else:
                    embed.add_field(name="Sorry", value=f"You've already accepted/ rejected *{challenge.title}*")
                    await ctx.send(embed=embed, hidden=True)
            else:
                embed.add_field(name="Error!", value="You do not have correct permission to accept or reject this challenge.")
                await ctx.send(embed=embed, hidden=True)
        else:
            embed.add_field(name="Error!", value="The challenge is already underway/ completed or cancelled.")
            await ctx.send(embed=embed, hidden=True)

    elif button_type == "chain-scan":

        await ctx.defer(hidden=True)

        scan_chain()

        if os.environ['CHECK_TNBC_CONFIRMATION'] == 'True':
            check_confirmation()

        match_transaction()

        obj, created = await sync_to_async(User.objects.get_or_create)(discord_id=str(ctx.author.id))

        embed = discord.Embed(title="Scan Completed")
        embed.add_field(name='New Balance', value=obj.get_decimal_balance())
        embed.add_field(name='Locked Amount', value=obj.get_decimal_locked_amount())
        embed.add_field(name='Available Balance', value=obj.get_decimal_available_balance())

        await ctx.send(embed=embed, hidden=True, components=[create_actionrow(create_button(custom_id="chain-scan", style=ButtonStyle.green, label="Scan Again?"))])

    else:
        await ctx.send("Where did you find this button??", hidden=True)


@slash.slash(name="kill", description="Kill the bot!!")
async def kill(ctx):

    await ctx.defer(hidden=True)

    if int(ctx.author.id) == int(settings.BOT_MANAGER_ID):
        print("Shutting Down the bot")
        await ctx.send("Bot Shut Down", hidden=True)
        await bot.close()
    else:
        await ctx.send("#DonotKillMaakayBot", hidden=True)

bot.run(TOKEN)
