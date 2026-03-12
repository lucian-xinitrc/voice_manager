import os, disnake
from dotenv import load_dotenv
from disnake.ext import commands
from disnake import TextInputStyle

load_dotenv()
bot = commands.Bot(
	intents=disnake.Intents.all(), 
	allowed_mentions=disnake.AllowedMentions(everyone=True)
)
lobby=1468746117259853869
gaming=1468746117259853870
create=1481647686288412813
voice_channels_id=[lobby, gaming, create]

class NameModal(disnake.ui.Modal):
    def __init__(self, member): 
        components = [
            disnake.ui.TextInput(
                label="channel_name",
                placeholder="Type the name of the channel",
                custom_id="channel_name",
                style=TextInputStyle.short,
                max_length=15,
            ),
        ]
        super().__init__(title="Name voice channel", components=components)

        self.member = member

    async def callback(self, inter: disnake.ModalInteraction):
        embed = disnake.Embed(title="Name your New Voice Channel")
        voice_id = self.member.voice.channel.id

        voice = bot.get_channel(voice_id)
        old_name = self.member.voice.channel.name
        channelName = inter.text_values.get("channel_name")

        await voice.edit(name=channelName)
        
        await inter.send(f"Channel named from `{old_name}` in `{channelName}` by `{self.member.name}`")

@bot.slash_command(description="Change generated voice channel's name")
async def change_voice_name(inter: disnake.AppCmdInter):
	member = inter.author
	voice_id = member.voice.channel.id
	if(voice_id not in voice_channels_id):
		await inter.response.send_modal(modal=NameModal(member))
	else:
		await inter.response.send_message("You don't have permission to change this!!!")

@bot.event
async def on_voice_state_update(member, before, after):
	try:
		channel_id = 1481616710829080708
		channel = bot.get_channel(channel_id)
		if(after.channel is not None):
			if(after.channel.id == 1481647686288412813):
				voice_id = after.channel.id
				voice = bot.get_channel(voice_id)
				channel_name = f"{member.name}'s channel"
				clone_channel = await voice.clone(name=channel_name)
				await member.move_to(clone_channel)
			else:
				if(before.channel is not None):
					voice_id = before.channel.id
					if(voice_id not in voice_channels_id):
						voice_chan = bot.get_channel(voice_id)
						if(not voice_chan.members):
							await voice_chan.delete()
		else:
			voice_id = before.channel.id
			if(voice_id not in voice_channels_id):
				voice_chan = bot.get_channel(voice_id)
				if(not voice_chan.members):
					await voice_chan.delete()
	except Exception as e:
		channel_id = 1481616710829080708
		channel = bot.get_channel(channel_id)
		await channel.send(f"[ VOICE CHAT - ERROR ] {e}")

@bot.event
async def on_ready():
	activity = disnake.Game(name="Scanning for messages...")
	await bot.change_presence(status=disnake.Status.idle, activity=activity)

if __name__ == "__main__":
	bot.run(os.getenv('bot_token'))