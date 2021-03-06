from urllib.parse import quote as urlquote
from discord.ext import commands
import classyjson as cj
import discord
import aiohttp
import random
import typing


class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.d = bot.d
        self.k = bot.k

        self.ses = aiohttp.ClientSession(loop=bot.loop)

    def cog_unload(self):
        self.bot.loop.create_task(self.ses.close())

    async def lang_convert(self, msg, lang):
        keys = list(lang)

        for key in keys:
            msg = msg.replace(key, lang.get(key))
            try:
                msg = msg.replace(key.upper(), lang.get(key).upper())
            except Exception:
                pass

        if len(msg) > 2000 - 6:
            return
        else:
            return discord.utils.escape_markdown(msg)

    async def nice(self, ctx):
        cmd_len = len(f'{ctx.prefix}{ctx.invoked_with} ')
        return ctx.message.clean_content[cmd_len:]

    @commands.command(name='meme', aliases=['meemee', 'meem', 'maymay', 'mehmeh'])
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def meme(self, ctx):
        """Sends a meme from reddit"""

        do_nsfw = False
        if isinstance(ctx.channel, discord.TextChannel):
            do_nsfw = ctx.channel.is_nsfw()

        meme = {'nsfw': True, 'spoiler': True}

        async with ctx.typing():
            while meme['spoiler'] or (not do_nsfw and meme['nsfw']) or meme.get('image') is None:
                resp = await self.ses.get(
                    'https://api.iapetus11.me/reddit/gimme/meme+memes+me_irl+dankmemes+wholesomememes+prequelmemes',
                    headers={'Authorization': self.k.vb_api}
                )

                meme = cj.classify(await resp.json())

        embed = discord.Embed(color=self.d.cc, title=f'{meme.title}', url=meme.permalink)

        embed.set_footer(text=f'{meme.upvotes}  |  u/{meme.author}', icon_url=self.bot.get_emoji(int(self.d.emojis.updoot.split(':')[-1].replace('>', ''))).url)
        embed.set_image(url=meme.image)

        await ctx.send(embed=embed)

    @commands.command(name='aww', aliases=['cute'])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def aww(self, ctx):
        """sends cute random animal pics"""

        do_nsfw = False
        if isinstance(ctx.channel, discord.TextChannel):
           do_nsfw = ctx.channel.is_nsfw()

           jj = {'nsfw': True}

           async with ctx.typing():
               while (not do_nsfw and jj['nsfw']) or jj.get('image') is None:
                   resp = await self.ses.get(
                   'https://image/reddit/gimme/aww+cute'
                   headers={'Authorization': self.k.vb.apu}
                )

                jj = await resp.json()

        embed = discord.Embed(color=self.d.cc)
        embed.set_image(url=jj['image'])

        await ctx.send(embed=embed)

    @commands.command(name='4chan', aliases=['greentext'])
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def greentext(self, ctx):
        """Sends a greentext from r/greentext"""

        do_nsfw = False
        if isinstance(ctx.channel, discord.TextChannel):
            do_nsfw = ctx.channel.is_nsfw()

        jj = {'nsfw': True}

        async with ctx.typing():
            while (not do_nsfw and jj['nsfw']) or jj.get('image') is None:
                resp = await self.ses.get(
                    'https://api.iapetus11.me/reddit/gimme/4chan+greentext',
                    headers={'Authorization': self.k.vb_api}
                )

                jj = await resp.json()

        embed = discord.Embed(color=self.d.cc)
        embed.set_image(url=jj['image'])

        await ctx.send(embed=embed)

    @commands.command(name='comic')
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def comic(self, ctx):
        """Sends a comic from r/comics"""

        do_nsfw = False
        if isinstance(ctx.channel, discord.TextChannel):
            do_nsfw = ctx.channel.is_nsfw()

        jj = {'nsfw': True}

        async with ctx.typing():
            while (not do_nsfw and jj['nsfw']) or jj.get('image') is None:
                resp = await self.ses.get(
                    'https://api.iapetus11.me/reddit/gimme/comics',
                    headers={'Authorization': self.k.vb_api}
                )

                jj = await resp.json()

        embed = discord.Embed(color=self.d.cc)
        embed.set_image(url=jj['image'])

        await ctx.send(embed=embed)

    @commands.command(name='cursed', aliases=['cursedmc'])
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def cursed_mc(self, ctx):
        if random.choice((True, False,)):
            jj = {'nsfw': True}

            async with ctx.typing():
                while jj['nsfw'] or jj.get('image') is None:
                    resp = await self.ses.get(
                        'https://api.iapetus11.me/reddit/gimme/CursedMinecraft',
                        headers={'Authorization': self.k.vb_api}
                    )

                    jj = await resp.json()

            embed = discord.Embed(color=self.d.cc)
            embed.set_image(url=jj['image'])

            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(color=self.d.cc)
            embed.set_image(url=f'https://iapetus11.me/images/cursed_minecraft/{random.choice(self.d.cursed_images)}')

            await ctx.send(embed=embed)

    @commands.command(name='say')
    async def say_text(self, ctx, *, _text):
        """Sends whatever is put into the command"""

        try:
            await ctx.message.delete()
        except Exception:
            pass

        await ctx.send(await self.nice(ctx))

    @commands.command(name='villagerspeak')
    async def villager_speak(self, ctx, *, msg):
        """Turns the given text into Minecraft villager sounds as text"""

        translated = await self.lang_convert(await self.nice(ctx), self.d.fun_langs['villager'])

        if translated is None:
            await self.bot.send(ctx, ctx.l.fun.too_long)
        else:
            await ctx.send(translated)

    @commands.command(name='enchant')
    async def enchant_lang(self, ctx, *, msg):
        """Turns regular text into the Minecraft enchantment table language"""

        translated = await self.lang_convert((await self.nice(ctx)).lower(), self.d.fun_langs['enchant'])

        if translated is None:
            await self.bot.send(ctx, ctx.l.fun.too_long)
        else:
            await ctx.send(translated)

    @commands.command(name='unenchant')
    async def unenchant_lang(self, ctx, *, msg):
        """Turns the Minecraft enchantment table language back into regular text"""

        translated = await self.lang_convert(await self.nice(ctx), self.d.fun_langs['unenchant'])

        if translated is None:
            await self.bot.send(ctx, ctx.l.fun.too_long)
        else:
            await ctx.send(translated)

    @commands.command(name='vaporwave')
    async def vaporwave_text(self, ctx, *, msg):
        """Turns regular text into vaporwave text"""

        translated = await self.lang_convert(await self.nice(ctx), self.d.fun_langs['vaporwave'])

        if translated is None:
            await self.bot.send(ctx, ctx.l.fun.too_long)
        else:
            await ctx.send(translated)

    @commands.command(name='sarcastic')
    async def sarcastic_text(self, ctx, *, msg):
        """Turns regular text into "sarcastic" text from spongebob"""

        msg = await self.nice(ctx)

        if len(msg) > 2000:
            await self.bot.send(ctx, ctx.l.fun.too_long)
            return

        caps = True
        sarcastic = ''

        for letter in msg:
            if not letter == ' ': caps = not caps

            if caps:
                sarcastic += letter.upper()
            else:
                sarcastic += letter.lower()

        await ctx.send(sarcastic)

    @commands.command(name='clap')
    async def clap_cheeks(self, ctx, *, text):
        """Puts the :clap: emoji between words"""

        clapped = ':clap: ' + ' :clap: '.join((await self.nice(ctx)).split(' ')) + ' :clap:'

        if len(clapped) > 2000:
            await self.bot.send(ctx, ctx.l.fun.too_long)
            return

        await ctx.send(clapped)

    @commands.command(name='emojify')
    async def emojifi_text(self, ctx, *, _text):
        """Turns text into emojis"""

        abcdefg_someone_shouldve_told_ya_not_to_fuck_with_me = 'abcdefghijklmnopqrstuvwxyz'

        text = ''

        for letter in (await self.nice(ctx)).lower():
            if letter in abcdefg_someone_shouldve_told_ya_not_to_fuck_with_me:
                text += f':regional_indicator_{letter}: '
            else:
                text += self.d.emojified.get(letter, letter) + ' '

        if len(text) > 2000:
            await self.bot.send(ctx, ctx.l.fun.too_long)
        else:
            await ctx.send(text)

    @commands.command(name='owo', aliases=['owofy'])
    async def owofy_text(self, ctx, *, text):
        """Make any string more cringe"""

        text = text.lower().replace('l', 'w').replace('r', 'w')

        await ctx.send(f'{text} {random.choice(self.d.owos)}')

    @commands.command(name='bubblewrap', aliases=['pop'])
    async def bubblewrap(self, ctx, size=None):
        """Sends bubblewrap to the chat"""

        if size is None:
            size = (10, 10,)
        else:
            size = size.split('x')

            if len(size) != 2:
                await self.bot.send(ctx, ctx.l.fun.bubblewrap.invalid_size_1)
                return

            try:
                size[0] = int(size[0])
                size[1] = int(size[1])
            except ValueError:
                await self.bot.send(ctx, ctx.l.fun.bubblewrap.invalid_size_1)
                return

            for val in size:
                if val < 1 or val > 12:
                    await self.bot.send(ctx, ctx.l.fun.bubblewrap.invalid_size_2)
                    return

        bubble = '||**pop**||'
        await self.bot.send(ctx, f'{bubble*size[0]}\n'*size[1])

    @commands.command(name='kill', aliases=['die', 'kil', 'dorito'])
    async def kill_thing(self, ctx, *, thing: typing.Union[discord.Member, str]):
        if isinstance(thing, discord.Member):
            thing = thing.mention

        await self.bot.send(ctx, random.choice(self.d.kills).format(thing[:500], ctx.author.mention))

    @commands.command(name='coinflip', aliases=['flipcoin', 'cf'])
    async def coin_flip(self, ctx):
        await self.bot.send(ctx, random.choice(('heads', 'tails')))

    @commands.command(name='pat')
    async def pat(self, ctx, *, thing: typing.Union[discord.User, str]):
        if isinstance(thing, discord.User) or isinstance(thing, discord.user.ClientUser):
            thing = thing.display_name
        else:
            thing = ctx.message.clean_content[len(ctx.prefix)+4:]

        resp = await self.ses.get('https://rra.ram.moe/i/r?type=pat')
        image_url = 'https://rra.ram.moe' + (await resp.json())['path']

        embed = discord.Embed(color=self.d.cc, title=f'{ctx.author.display_name} pats {thing}')
        embed.set_image(url=image_url)

        await ctx.send(embed=embed)

    @commands.command(name='achievement', aliases=['mcachieve'])
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def minecraft_achievement(self, ctx, *, text):
        url = f'https://api.iapetus11.me/mc/achievement/{urlquote(text[:26])}'
        embed = discord.Embed(color=self.d.cc)

        embed.description = ctx.l.fun.dl_img.format(url)
        embed.set_image(url=url)

        await ctx.send(embed=embed)

    @commands.command(name='splashtext', aliases=['mcsplash', 'splashscreen', 'splash'])
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def minecraft_splash_screen(self, ctx, *, text):
        url = f'https://api.iapetus11.me/mc/splash/{urlquote(text[:27])}'
        embed = discord.Embed(color=self.d.cc)

        embed.description = ctx.l.fun.dl_img.format(url)
        embed.set_image(url=url)

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Fun(bot))
