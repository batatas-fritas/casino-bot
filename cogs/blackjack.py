import sys
sys.path.append("/home/francisco/Documents/discord-bot/casino-bot")
import discord
from discord.ext import commands
from user import User
from util.deck import Deck
import time
        

class BlackJackGame(discord.ui.View):
    def __init__(self, user: User, ctx: discord.ApplicationContext, bet: int) -> None:
        super().__init__()
        self.user = user
        self.ctx = ctx
        self.deck = Deck()
        self.bet = bet
        self.dealer = []
        self.player = []

    def getPlayerEmbed(self):
        embed = discord.Embed(
            color=discord.Colour.yellow(),
            title="Player's hand",
        )
        for card in self.player:
            embed.add_field(name=card.toString(), value=card.suit)
        return embed
    
    def getDealersEmbed(self):
        embed = discord.Embed(
            color=discord.Colour.yellow(),
            title="Dealer's hand",
        )
        for card in self.dealer:
            embed.add_field(name=card.toString(), value=card.suit)
        return embed
    
    def calculatePlayerCards(self) -> int:
        result = 0
        ace = 0
        for card in self.player:
            if card.getBlackjackValue() == 11:
                ace +=1
            result += card.getBlackjackValue()
        while(ace > 0 and result > 21):
            result -= 10
            ace -= 1
        return result

    def calculateDealersCards(self) -> int:
        result = 0
        ace = 0
        for card in self.dealer:
            if card.getBlackjackValue() == 11:
                ace +=1
            result += card.getBlackjackValue()
        while(ace > 0 and result > 21):
            result -= 10
            ace -= 1
        return result

    async def start(self):
        self.player.append(self.deck.takeCard())
        self.player.append(self.deck.takeCard())
        self.dealer.append(self.deck.takeCard())
        await self.gameloop()


    @discord.ui.button(label="Hit", style=discord.ButtonStyle.success)
    async def hit_callback(self, button, interaction: discord.Interaction):
        if interaction.user.id != self.user.id: return
        await interaction.message.delete()
        self.player.append(self.deck.takeCard())
        await self.gameloop()


    @discord.ui.button(label="Stand", style=discord.ButtonStyle.red)
    async def stand_callback(self, button, interaction: discord.Interaction):
        if interaction.user.id != self.user.id: return
        message = interaction.message
        while(self.calculateDealersCards() < self.calculatePlayerCards() and self.calculateDealersCards() < 16):
            self.dealer.append(self.deck.takeCard())
            await message.delete()
            message = await interaction.channel.send(embeds=[self.getDealersEmbed(), self.getPlayerEmbed()])
            time.sleep(0.2)
        await message.delete()
        await self.calculateWinner(message.channel)


    async def calculateWinner(self, channel):
        if self.calculateDealersCards() > 21 or self.calculateDealersCards() < self.calculatePlayerCards(): # dealer bust
            await self.win(channel, False)
            return
        if self.calculateDealersCards() > self.calculatePlayerCards(): # dealer wins
            await self.lose(channel)
            return
        else:
            await self.draw(channel)
            return
        

    async def gameloop(self):
        playerScore = self.calculatePlayerCards()
        if playerScore == 21:
            await self.win(self.ctx.channel, True)
        if playerScore > 21: # player busted
            await self.lose(self.ctx.channel)
        else:
            await self.ctx.respond(embeds=[self.getDealersEmbed(), self.getPlayerEmbed()], view=self)
    
    async def win(self, channel, blackjack):
        print("Player wins")
        await channel.send("You win", embeds=[self.getDealersEmbed(), self.getPlayerEmbed()])
        if blackjack:
            self.user.updateBalance(self.bet*1.5)
        else:
            self.user.updateBalance(self.bet)
        return

    async def lose(self, channel):
        print("Player loses")
        await channel.send("You lose, sit kid", embeds=[self.getDealersEmbed(), self.getPlayerEmbed()])
        self.user.updateBalance(-self.bet)
        return

    async def draw(self, channel):
        print("Draw")
        await channel.send("Draw", embeds=[self.getDealersEmbed(), self.getPlayerEmbed()])
        return
        

class BlackJackCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(name="blackjack", description="starts a new game of blackjack")
    @discord.option(
        "bet",
        int,
        description = "The amount of money you want to bet",
        required = True
    )
    async def setup_game(self, ctx: discord.ApplicationContext, bet: int):
        print(f"{ctx.user.name} has bet {bet}$")
        user = User(ctx.user.id, ctx.user.name)
        if user.balance < bet: 
            await ctx.respond("You don't have enough money pookie.", ephemeral=True)
            return
        if bet <= 0:
            await ctx.respond("You can't bet that amount of money pookie.", ephemeral=True)
            return
        blackjack = BlackJackGame(user, ctx, bet)
        await blackjack.start()



def setup(bot):
    bot.add_cog(BlackJackCog(bot))