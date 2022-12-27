from captcha.image import ImageCaptcha
import discord, random, os, asyncio

bot = discord.Bot()

@bot.event
async def on_ready():
  print(bot.user)

@bot.slash_command(name="verify")
async def verify(ctx):
  image = ImageCaptcha(width=260, height=90)
  captcha_text = ''.join(
  random.choices([line.strip() for line in open('abc.txt', 'r')], k=5))
  
  data = image.generate(captcha_text)
  role = discord.utils.get(ctx.guild.roles, name="verfied")

  if role is ctx.author.roles:
    await ctx.author.send("verfied", ephemeral=True)
  else:
    await ctx.respond("check dms", ephemeral=True)
    image.write(captcha_text, f'{ctx.author.name}#{ctx.author.discriminator}.png')
    embed = discord.Embed(title="Verification", description="please write the words above ")
    file = discord.File(f'{ctx.author.name}#{ctx.author.discriminator}.png')
    await ctx.author.send(file=file, embed=embed)
    while True:
      try:
        msg = await bot.wait_for("message", timeout = 5, check=lambda check: check.author.id == ctx.author.id)
        if msg.content == captcha_text:
          await msg.reply("verfied")
          await ctx.author.add_roles(role)
          os.unlink(f'{ctx.author.name}#{ctx.author.discriminator}.png')
        else:
           await msg.reply("Incorrect")
      except asyncio.TimeoutError:
        await ctx.send("timed out")
        os.unlink(f'{ctx.author.name}#{ctx.author.discriminator}.png')
        
bot.run(os.environ['TOKEN']) #os.environ['TOKEN'] -> Go to secrets
