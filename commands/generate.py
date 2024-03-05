import disnake
from disnake.ext import commands
import random
import string
import os

class GenerateCommand(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command(
        name="generate",
        description="Generate role codes",
    )
    @commands.default_member_permissions(manage_roles=True)
    async def generate(self,
                   inter: disnake.ApplicationCommandInteraction,
                   role: disnake.Role,
                   number: int = 1,
                   length: int = 8):
        # Generate Codes
        codes = [''.join(random.choices(string.ascii_uppercase + string.digits, k=length)) for _ in range(number)]

        codesAndRoleList = []
        for i in range(len(codes)):
          codesAndRoleList.append(codes[i] + " " + str(role.id))
          i += 1
        # Save the Data
        with open(os.path.join('data/', str(inter.guild.id)), 'a') as f:
          for item in codesAndRoleList:
            f.write(item + "\n")
      
        # Check if codes can be sent directly
        if number * length < 1512:
            await inter.response.send_message(content="Generated Codes:\n" + "\n".join(codes), ephemeral=True)
        else:
            # Ensure Temp directory exists
            temp_dir = 'Temp'
            os.makedirs(temp_dir, exist_ok=True)

            # Generate a unique filename
            filename = ''.join(random.choices(string.ascii_uppercase + string.digits, k=32)) + ".txt"
            file_path = os.path.join(temp_dir, filename)

            # Write codes to file
            with open(file_path, 'w') as f:
                for code in codes:
                    f.write(f"{code}\n")

            # Send the file
            with open(file_path, 'rb') as file_to_send:
                await inter.response.send_message(content="I couldn't fit all the codes in, so I packed them neatly into a file for you!", file=disnake.File(file_to_send, filename=role.name + '_codes.txt'))
            # Delete the file
            os.remove(file_path)



def setup(bot: commands.Bot):
  bot.add_cog(GenerateCommand(bot))
