import db
import discord

class User:
    def __init__(self, id, username) -> None:
        self.id = id
        self.username = username
        self.balance = self.getBalance()
    
    def getBalance(self):
        balance = db.get_user_balance(self.id)
        if balance == None:
            db.create_user(self.id, self.username)
            balance = db.get_user_balance(self.id)
        return balance
    
    def getUserEmbed(self):
        embed = discord.Embed(color=discord.Colour.yellow(), 
                              title=self.username, 
                              description=str(self.balance) + "$")
        return embed
    
    def updateBalance(self, quantity):
        self.balance += quantity
        db.update_user_balance(self.id, self.balance)
        return
