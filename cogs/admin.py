from asgiref.sync import sync_to_async
from discord.ext import commands
from discord_slash import cog_ext
from discord_slash.utils.manage_commands import create_option
from core.models.guild import Guild
from discord.ext.commands.errors import MissingRole

class admin(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


    @cog_ext.cog_subcommand(base="admin", name="set_withdrawl_address", description="Set withdrawl adress for the server", options=[
        create_option(name="address", description="Withdrawl address", required=True, option_type=3)
    ])
    async def admin_set_withdrawl_address(self, ctx, address):

        has_role = False

        for role in ctx.author.roles:
            if role.name == "Maakay Bot Admin":
                has_role = True
                break
        
        if has_role:
            if len(address) == 64:
                guild, created = await sync_to_async(Guild.objects.get_or_create)(guild_id=str(ctx.guild.id))
                guild.withdrawal_address = address
                guild.save()

                await ctx.send(f"Withdrawl address for **{ctx.guild.name}** set to `{address}` successfully!")
            else:
                await ctx.send("Invalid Withdrawl Address!")
        else:
            await ctx.send("You don't have the required `Maakay Bot Admin` Role!!")


def setup(bot):
    bot.add_cog(admin(bot))