import disnake
from disnake.ext import commands
import os
import mmap

def find_and_delete_code(code, filename):
  # Open the file in read-write mode
  with open(filename, 'r+b') as f:
      # Memory-map the file, size 0 means whole file
      with mmap.mmap(f.fileno(), length=0, access=mmap.ACCESS_WRITE) as mm:
          # Convert the code to bytes and search
          code_bytes = bytes(code + ' ', 'utf-8')
          start = mm.find(code_bytes)

          if start != -1:
              # Find the end of the line
              end = mm.find(b'\n', start)
              # If the code is at the end of the file without a newline
              if end == -1:
                  end = len(mm)
              else:
                  # Move the end past the newline character if it's not at the end of the file
                  end += 1

              # Extract the whole line (convert it to a string) BEFORE modifying the mmap object
              line = mm[start:end].decode('utf-8')
              _, id_str = line.strip().split(' ', 1)

              # Prepare the content without the found line
              mm.seek(0)  # Go to the beginning
              content_before = mm[:start]  # Content before the found line
              content_after = mm[end:] if end < len(mm) else b''  # Content after the found line

              # Calculate the new content length
              new_content_length = len(content_before) + len(content_after)

              # Truncate and write back the modified content
              mm.seek(0)
              mm.write(content_before + content_after)
              mm.flush()
              f.truncate(new_content_length)  # Adjust file size

              return id_str
          else:
              return None

class RedeemCommand(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command(
        name="redeem",
        description="Redeem a code to get a role!",
    )
    async def redeem(self, inter: disnake.ApplicationCommandInteraction, code: str):
        numId_str = find_and_delete_code(code, os.path.join('data/', str(inter.guild.id)))
             
        if not numId_str:
            await inter.response.send_message("406 Not Acceptable: The Code you entered is Invalid, or was redeemed already!", ephemeral=True)
            return
        
        try:
            numId = int(numId_str)
        except ValueError:
            await inter.response.send_message("Error: The role ID associated with this code is not a valid number.", ephemeral=True)
            return

        redeemedRole = inter.guild.get_role(numId)
      
        if redeemedRole is None:
            await inter.response.send_message("404 Not Found: The role associated with this code does not exist.", ephemeral=True)
            return
        if not inter.guild.me.guild_permissions.manage_roles:
          await inter.response.send_message("I don't have permissions to manage roles.", ephemeral=True)
          return

        role = redeemedRole

        # Check if the bot's highest role is above the role it's trying to assign
        if role.position >= inter.guild.me.top_role.position:
          await inter.response.send_message("I can't manage this role because it's equal to or higher than my highest role. Reach out to the admins to fix it!", ephemeral=True)
          return

        await inter.author.add_roles(redeemedRole)
        await inter.response.send_message(f"The role <@&{numId}> has been added!", ephemeral=True)

def setup(bot: commands.Bot):
    bot.add_cog(RedeemCommand(bot))
