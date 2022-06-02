from pickle import TRUE
import discord
import aiohttp
import random

from discord.ext import commands 

intents = discord.Intents().all()
intents.members = True

# Retire la commande help par défaut pour en utilisé une que l'on créer nous même
client = commands.Bot(command_prefix="!", help_command=None, intents = intents)
client.remove_command('help') 

# Liste permettant de sauvegarder la conversation
saveConversation = []
saveAnswer = []

one = False

# Arbre binaire
class Node :
    def __init__(self,question,keyword,list_child_node):
        self.question = question
        self.keyword = keyword
        self.list_child_node = list_child_node

first_node = Node("tapez $aidebot pour démarer la conversation",".",[Node("Comment puis je vous aider ? \n Tapez `1` : si vous cherchez un cours de codage \n Tapez `2` : si vous cherchez une documentation \n Tapez `3` : si vous rencontrez un autre problème \n Tapez `4` : si vous voulez recommencer la conversation \n ","$aidebot",[
    Node("`Python` \n`Javascript` \n`HTML` \n`CSS` \n`PHP`","1",[
        Node("Voici ton tuto Python : https://www.youtube.com/watch?v=LamjAFnybo0&t=199s","python",[]),
        Node("Voici ton tuto Javascript : https://www.youtube.com/watch?v=UEHyHxqbtyg","javascript",[]),
        Node("Voici ton tuto HTML: https://www.youtube.com/watch?v=qsbkZ7gIKnc","html",[]),
        Node("Voici ton tuto CSS : https://www.youtube.com/watch?v=HDobHQfbRbo","css",[]),
        Node("Voici ton tuto PHP : https://www.youtube.com/watch?v=nu2m9HaeVV4","php",[]),
    ]),
    Node("Sur quelles languages cherchez vous une doccumentation  ?","2",[
        Node("Voici ta documentation Python : https://www.w3schools.com/python/default.asp","python",[]),
        Node("Voici ta documentation Javascript : https://www.w3schools.com/js/default.asp","javascript",[]),
        Node("Voici ta documentation HTML : https://www.w3schools.com/TAgs/default.asp","html",[]),
        Node("Voici ta documentation CSS : https://www.w3schools.com/css/default.asp","css",[]),
        Node("Voici ta documentation PHP : https://www.w3schools.com/php/default.asp","php",[])
    ]),

])])

current_node = first_node
precedent_node = current_node
rebegin_node = first_node

# Fonction traitant les messages
@client.event
async def on_message(message):
    global current_node
    global precedent_node
    Help_channel = client.get_channel(1)
    message.content = message.content.lower()
    # Event qui empêche le bot de se répondre a lui même
    if message.author == client.user:
        return

    # Permet d'avancer dans l'arbre, et sauvegarder la conversation
    for child in current_node.list_child_node:
        if child.keyword in message.content.lower():
            saveConversation.append(message.content)
            precedent_node = current_node
            await message.channel.send(child.question)
            current_node = child
            saveAnswer.append(child.question)
            return

        # Revenir au message précédent dans l'arbre
        if message.content == "retour":
            current_node = precedent_node
            await message.channel.send(current_node.question)
            return

        if message.content == "4":
            current_node = rebegin_node
            await message.channel.send(current_node.question)
            return


    # Afficher toute la conversation avec le bot
    if message.channel == Help_channel and message.content == 'où':
        i = 0
        while i < len(saveConversation) and i < len(saveAnswer):
            await Help_channel.send("Vous m'avez dit : " + saveConversation[i])
            await Help_channel.send("Je vous ai répondu : " + saveAnswer[i])
            i += 1
    
    
    # Event pour dire bonjour aux utilisateurs
    if message.content == 'bonjour' or message.content == 'salut' or message.content == 'coucou' or message.content == 'yo':
        await message.channel.send(f"Bonjour {message.author.mention} si tu as besoin d'aide tape `!help`")

    await client.process_commands(message)

# Commande permettant de se donner le rôle de membre ou de se retirer le rôle de membre
@client.command(name='membre')
async def role(ctx):
    membre = discord.utils.get(ctx.guild.roles, id=1)
    # Condition pour vérifier si la personne est déjà membre, modérateur ou aucun des deux
    if membre in ctx.author.roles:
        await ctx.author.remove_roles(membre)
        await ctx.send("Vous n'êtes plus membre !")
    else:
        await ctx.author.add_roles(membre)
        await ctx.send("Vous êtes désormais membre !")

# Lorsqu'un membre rejoint le bot lui explique ce qu'est la commande !help pour qu'il ai accès à toutes les commandes
@client.event
async def on_member_join(member):
    channel = client.get_channel(1)
    await channel.send(f"Bonjour {member.mention} si tu as besoin d'aide tape `$aidebot` et pour accéder aux commandes du bot tape `!help`")

# Commande pour supprimer un certain nombre de messages
@client.command(name='del')
async def delete(ctx, number_of_messages: int):
    moderator = discord.utils.get(ctx.guild.roles, id=1)
    # Condition pour que seul les modérateurs puissent utiliser cette commande
    if moderator in ctx.author.roles:
        messages = await ctx.channel.history(limit=number_of_messages + 1).flatten()

        for each_message in messages:
            await each_message.delete()

# Commande pour ping un modérateur
@client.command(name='modo')
async def ping(ctx):
    moderator = discord.utils.get(ctx.guild.roles, id=1)
    membre = discord.utils.get(ctx.guild.roles, id=1)
    #Conditions de rôles pour pouvoir utiliser la commande
    if membre in ctx.author.roles or moderator in ctx.author.roles:
        await ctx.send("J'appelle un " + f'{moderator.mention}')

# Commande qui décrit les commandes utilisable avec le bot
@client.command('help')
async def help(ctx):
    await ctx.send("```COMMANDES DU BOT :\n \n !del + <nombre> : Supprime le nombre de message demandé. \n Ne peux être utilisé que par un utilisateur ayant le rôle de modérateur. \n \n !modo : Mentionne tout les modérateurs pour aider un utilisateur dans le besoin. \n Ne peux être utilisé que par un utilisateur ayant le rôle de modérateur. \n \n !membre : te permet de devenir un membre et avoir accès à la plupart des commandes. \n \n !chien : Envoi l'image d'un bon chien chien. \n Ne peux être utilisé que par un utilisateur ayant le rôle de membre ou modérateur. \n \n !def + <mot> : Permet de rediriger vers la définition d'un mot. \n Ne peux être utilisé que par un utilisateur ayant le rôle de membre ou modérateur. \n \n !battle + <@nom d'un membre du serveur> : Permet de lancer un combat entre deux membres du serveur. Combattre le bot est possible mais il ne se laisse pas faire... \n Ne peux être utilisé que par un utilisateur ayant le rôle de membre ou modérateur. \n \n $aidebot : Permet d'avoir une conversation d'aide avec le bot. \n Ne peux être utilisé que par un utilisateur ayant le rôle de membre ou modérateur.```")

# Commande donnant la définition Larousse des mots voulus
@client.command('def')
async def definition(ctx, mot):
    moderator = discord.utils.get(ctx.guild.roles, id=1)
    membre = discord.utils.get(ctx.guild.roles, id=1)
    if membre in ctx.author.roles or moderator in ctx.author.roles:
        await ctx.send("Voici un lien pour la défintion du mot :" + mot + " https://www.larousse.fr/dictionnaires/francais/" + mot +"/")

# Commande renvoyant une image de chien
@client.command('chien')
async def dog(ctx):
   async with aiohttp.ClientSession() as session:
      request = await session.get('https://some-random-api.ml/img/dog') #Lien contenant des images aléatoire de chien
      dogjson = await request.json() #Convertis en JSON
   image = discord.Embed(title="Bon toutou !") #Creer un embed
   image.set_image(url=dogjson['link'])
   moderator = discord.utils.get(ctx.guild.roles, id=1)
   membre = discord.utils.get(ctx.guild.roles, id=1)
   if membre in ctx.author.roles or moderator in ctx.author.roles:
       await ctx.send(embed=image) # envoie l'image du chien

# Commande de combat entre 2 utilisateurs du discord
@client.command('battle')
async def battle(ctx, user: discord.Member):
    # Variable pour l'effet tour par tour du combat
    turn = 0
    # Points de vie du joueur 1
    Hp1 = 30
    # Points de vie du joueur 2
    Hp2 = 30
    # Points de vie de bloupi (bot)
    Hp3 = 80
    # Nombre de potions du joueur 1
    potionA = 3
    # Nombre de potions du joueur 2
    potionB =3
    # Nombre de potions du joueur 3 (bot)
    potionC = 1
    # Variable pour définir le joueur 2 (celui qui se fait mentionner par le joueur 1)
    user = user.mention
    # Variable pour définir le joueur 1 (celui qui fait la commande)
    P1 = ctx.message.author.mention
    moderator = discord.utils.get(ctx.guild.roles, id=1)
    membre = discord.utils.get(ctx.guild.roles, id=1)
    

    # Conditions pour que la commande ne soit pas utilisable si on n'est pas membre ou modérateur
    if membre in ctx.author.roles or moderator in ctx.author.roles:
        # Condition pour que l'on ne puisse pas se ping soit même
        if user == P1:
            await ctx.send(f"Vous ne pouvez pas vous battre contre vous même {P1}")
        # Combat vs le bot
        elif client.user.mentioned_in(ctx.message):
            await ctx.send(f'{P1} vs {user}, que le meilleur gagne ! Autant te prévenir, je suis une tricheuse, bonne chance tu en aura besoin ;)')
            # Boucle tant que personne n'a plus de point de vie
            while Hp1 > 0 and Hp3 > 0:
                # Condition pour le tour du joueur 1
                if turn == 0:
                    await ctx.send(f'{P1}: `Attack, Heal,`  `Surrender` (la meilleure option pour toi :p)')
                    def check(m):
                        return m.content == 'attack' or m.content == 'Attack' or m.content == 'heal' or m.content == 'Heal' or m.content == 'surrender' or m.content == 'Surrender' and m.author == ctx.message.author

                    response = await client.wait_for('message', check=check)
                    # Condition pour le contenu du message renvoyé (bug à régler : tout le monde peu répondre et pas seulement le joueur concerné ! Vient peut-être de la def check au dessus)
                    if ("attack" in response.content or "Attack" in response.content):
                        # Condition si le joueur 2 est en vie
                        if Hp3 > 0:
                            # Création de la variable de dégats aléatoires
                            dmg = [0,1,2,3,4,5,6,7,8,9,10,11,12]
                            dmg = (random.choice(dmg))
                            Hp3 = Hp3 - dmg
                            # Messages différents en fonction des dégats
                            if dmg <= 0:
                                await ctx.send(f"{user} **esquive** l'attaque ! Bien essayé mais raté hahaha ! Il me reste **{Hp3}** points de vie :p")
                            if dmg >= 8 and dmg <11:
                                await ctx.send(f"{P1} assène un **coup critique** de **{dmg}** dégats ! Pas mal haha, mais il me reste toujours **{Hp3}** points de vie x)")
                            if dmg == 2:
                                await ctx.send(f"{P1} manque de précision et son coup ne fait que **{dmg}** de dégats. Il me reste **{Hp3}** points de vie. Tu peux mieux faire j'en suis sûr, courage :')")
                            if dmg >=3 and dmg <=7:
                                await ctx.send(f"{P1} inflige **{dmg}** de dégats. Il reste **{Hp3}** points de vie à {user}.")
                            if dmg == 1:
                                await ctx.send(f"{P1} manque de précision et son coup ne fait que.. Que **{dmg}** de dégat. Il me reste **{Hp3}** points de vie.. Au moins tu ne pourras pas faire pire... C'est déjà ça :')")
                            # Condition pour donner le tour au joueur 2
                            turn = 1
                            if dmg >= 11:
                                await ctx.send(f"{P1} assène un **coup critique** de **{dmg}** dégats qui paralyse son adversaire! Il reste **{Hp3}** points de vie à {user} qui perd un tour.")   
                                turn = 0 
                            # Condition de victoire (joueur 2 n'a plus de points de vie)
                            if Hp3 <= 0:
                                await ctx.send(f"**{P1} ... Remporte le match** ?!?! Contre l'être parfait que je suis ?? Impossible.. Je refuse de l'admettre... Tu as triché è_é")
                                break
                        elif Hp3 <= 0:
                            await ctx.send(f"**{P1} ... Remporte le match** ?!?! Contre l'être parfait que je suis ?? Impossible.. Je refuse de l'admettre... Tu as triché è_é")
                            break
                    # Conditions comme pour attack mais pour le heal    
                    if ("heal" in response.content or "Heal" in response.content):
                        # Messages différents en fonction des pv du joueur et du nombre de potions
                        if Hp1 >= 30 and potionA >=1:
                            potionA = potionA -1
                            await ctx.send(f"{P1} à déjà **{Hp1}** points de vie, il/elle perd son tour (Mdrrr tu fais exprès ?). Il lui reste {potionA} potions.")
                            turn = 1
                        if potionA <= 0:
                            await ctx.send(f"{P1} n'a plus de potions, il/elle perd son tour. Voilà qui est bien dommage :p")
                            turn = 1
                        if Hp1 <30 and potionA >0:
                            # Variable pour redonner un nombre aléatoire de points de vie au joueur
                            potion = [3, 4, 5, 6, 7, 8, 9, 10]
                            potion = (random.choice(potion))
                            Hp1 = Hp1 + potion
                            if Hp1 > 30:
                                Hp1 = 30
                            potionA = potionA -1
                            await ctx.send(f"{P1} utilise une **potion** et récupère **{potion}** points de vie. Il lui reste maintenant **{Hp1}** points de vie et {potionA} potions. Mais ça ne te sauvera pas x)")
                            
                            turn = 1
                    # Conditions comme pour attack et heal mais pour surrender
                    if ("surrender" in response.content or "Surrender" in response.content):
                        await ctx.send(f"{P1} abandonne avec **{Hp1}** point de vie restants. {user} remporte le match avec **{Hp3}** points de vie restants. Tu admets enfin ma supériorité ! C'est la bonne décision ;)")
                        Hp1 = Hp1 - 30
                        Hp3 = Hp3 - 80
                        turn = turn + 1
                        break
                # Tour du joueur 2 (même commentaires que pour le joueur 1)
                elif turn == 1:
                    await ctx.send(f'{user}: `Attack, Heal, Surrender`')
                    if Hp1 > 0 and Hp3 >=50:
                        dmg = [0,4,5,6,7,8,9,10,11,12,13,14]
                        dmg = (random.choice(dmg))
                        Hp1 = Hp1 - dmg
                        if dmg <= 0:
                            await ctx.send(f"{P1} esquive l'attaque ! Bien joué il reste **{Hp1}** points de vie à {P1}. Mais tu ne fais que retarder l'inévitable :p")
                        if dmg >= 10 and dmg <13:
                            await ctx.send(f"{user} assène un **coup critique** de **{dmg}** dégats ! Il reste **{Hp1}** points de vie à {P1}.")
                        if dmg == 4:
                            await ctx.send(f"{user} manque de précision et son coup ne fait que **{dmg}** de dégats. Il reste **{Hp1}** points de vie à {P1}.")
                        if dmg >=5 and dmg <10:
                            await ctx.send(f"{user} inflige **{dmg}** de dégats."f" Il reste **{Hp1}** points de vie à {P1}.")
                        turn = turn - 1
                        if dmg == 13:
                            await ctx.send(f"{user} assène un **coup critique** de **{dmg}** dégats qui paralyse son adversaire! Il reste **{Hp1}** points de vie à {P1} qui perd un tour.")   
                            turn = 1 
                        if dmg == 14:
                            await ctx.send(f"{user} assène un **coup critique** de **{dmg}** dégats qui paralyse son adversaire! Il reste **{Hp1}** points de vie à {P1} qui perd un tour.")   
                            turn = 1 
                        if Hp1 <= 0:
                            await ctx.send(f"**{user} remporte le match.** Mais c'était une évidence, je suis la plus forte après tout UwU")
                            break
                    elif Hp1 <= 0:
                        await ctx.send(f"**{user} remporte le match.** Mais c'était une évidence, je suis la plus forte après tout UwU")
                        break
                    if Hp3 <50 and potionC >0:
                        potion = [3, 4, 5, 6, 7, 8, 9, 10]
                        potion = (random.choice(potion))
                        Hp3 = Hp3 + potion
                        if Hp3 > 80:
                            Hp3 = 80
                        potionC = potionC - 1
                        await ctx.send(f"{user} utilise une **potion** et récupère **{potion}** points de vie. Il lui reste maintenant **{Hp3}** points de vie et {potionC} potions.")
                        turn = 0


                    if Hp1 > 0 and potionC == 0 and turn == 1:
                        dmg = [0,4,5,6,7,8,9,10,11,12,13,14]
                        dmg = (random.choice(dmg))
                        Hp1 = Hp1 - dmg
                        if dmg <= 0:
                            await ctx.send(f"{P1} esquive l'attaque ! Bien joué il reste **{Hp1}** points de vie à {P1}. Mais tu ne fais que retarder l'inévitable :p")
                        if dmg >= 10 and dmg <13:
                            await ctx.send(f"{user} assène un **coup critique** de **{dmg}** dégats ! Il reste **{Hp1}** points de vie à {P1}.")
                        if dmg == 4:
                            await ctx.send(f"{user} manque de précision et son coup ne fait que **{dmg}** de dégats. Il reste **{Hp1}** points de vie à {P1}.")
                        if dmg >=5 and dmg <10:
                            await ctx.send(f"{user} inflige **{dmg}** de dégats."f" Il reste **{Hp1}** points de vie à {P1}.")
                        turn = 0
                    
                    if dmg >= 13:
                        await ctx.send(f"{user} assène un **coup critique** de **{dmg}** dégats qui paralyse son adversaire! Il reste **{Hp1}** points de vie à {P1} qui perd un tour.")   
                        turn = 1 
                    if Hp1 <= 0:
                        await ctx.send(f"**{user} remporte le match.** Mais c'était une évidence, je suis la plus forte après tout UwU")
                        break
                    if Hp3 <= 5 and potionC == 0 and Hp1 >= 10:
                        await ctx.send(f"{user} abandonne avec **{Hp2}** point de vie restants. {P1} remporte le match avec **{Hp1}** points de vie restants. Voilà t'es content ? J'abandonne tu triches :'(")
                        Hp1 = Hp1 - Hp1
                        Hp3 = Hp3 - Hp3
                        turn = -1
                        break

        else:
            await ctx.send(f'{P1} vs {user}, que le meilleur gagne !')
            # Boucle tant que personne n'a plus de point de vie
            while Hp1 > 0 and Hp2 > 0:
                # Condition pour le tour du joueur 1
                if turn == 0:
                    await ctx.send(f'{P1}: `Attack, Heal, Surrender`')
                    def check(m):
                        return m.content == 'attack' or m.content == 'Attack' or m.content == 'heal' or m.content == 'Heal' or m.content == 'surrender' or m.content == 'Surrender' and m.author == ctx.message.author

                    response = await client.wait_for('message', check=check)

                    # Condition pour le contenu du message renvoyé (bug à régler : tout le monde peu répondre et pas seulement le joueur concerné ! Vient peut-être de la def check au dessus)
                    if ("attack" in response.content or "Attack" in response.content):
                        # Condition si le joueur 2 est en vie
                        if Hp2 > 0:
                            # Création de la variable de dégats aléatoires
                            dmg = [0,1,2,3,4,5,6,7,8,9,10,11,12]
                            dmg = (random.choice(dmg))
                            Hp2 = Hp2 - dmg
                            # Messages différents en fonction des dégats
                            if dmg <= 0:
                                await ctx.send(f"{user} **esquive** l'attaque ! Il reste **{Hp2}** points de vie à {user}.")
                            if dmg >= 8 and dmg < 11:
                                await ctx.send(f"{P1} assène un **coup critique** de **{dmg}** dégats ! il reste **{Hp2}** points de vie à {user}.")                          
                            if dmg == 2:
                                await ctx.send(f"{P1} manque de précision et son coup ne fait que **{dmg}** de dégats. Il reste **{Hp2}** points de vie à {user}.")
                            if dmg >=3 and dmg <=7:
                                await ctx.send(f"{P1} inflige **{dmg}** de dégats. Il reste **{Hp2}** points de vie à {user}.")
                            if dmg == 1:
                                await ctx.send(f"{P1} manque de précision et son coup ne fait que **{dmg}** de dégat. Il reste **{Hp2}** points de vie à {user}.")
                            # Condition pour donner le tour au joueur 2
                            turn = turn +1
                            if dmg >= 11:
                                await ctx.send(f"{P1} assène un **coup critique** de **{dmg}** dégats qui paralyse son adversaire! Il reste **{Hp2}** points de vie à {user} qui perd un tour.")   
                                turn = 0                         
                            # Condition de victoire (joueur 2 n'a plus de points de vie)
                            if Hp2 <= 0:
                                await ctx.send(f"**{P1} remporte le match**.")
                                break
                        elif Hp2 <= 0:
                            await ctx.send(f"**{P1} remporte le match**.")
                            break
                    # Conditions comme pour attack mais pour le heal    
                    if ("heal" in response.content or "Heal" in response.content):
                        # Messages différents en fonction des pv du joueur et du nombre de potions
                        if Hp1 >= 30 and potionA >=1:
                            potionA = potionA -1
                            await ctx.send(f"{P1} à déjà **{Hp1}** points de vie, il/elle perd son tour. Il lui reste {potionA} potions.")
                            turn = 1
                        if potionA <= 0:
                            await ctx.send(f"{P1} n'a plus de potions, il/elle perd son tour.")
                            turn = 1
                        if Hp1 <30 and potion >0:
                            # Variable pour redonner un nombre aléatoire de points de vie au joueur
                            potion = [3, 4, 5, 6, 7, 8, 9, 10]
                            potion = (random.choice(potion))
                            Hp1 = Hp1 + potion
                            if Hp1 > 30:
                                Hp1 = 30
                            potionA = potionA -1
                            await ctx.send(f"{P1} utilise une **potion** et récupère **{potion}** points de vie. Il lui reste maintenant **{Hp1}** points de vie et {potionA} potions.")
                            
                            turn = 1
                    # Conditions comme pour attack et heal mais pour surrender
                    if ("surrender" in response.content or "Surrender" in response.content):
                        await ctx.send(f"{P1} abandonne avec **{Hp1}** point de vie restants. {user} remporte le match avec **{Hp2}** points de vie restants.")
                        Hp1 = Hp1 - 30
                        Hp2 = Hp2 - 30
                        turn = turn + 1
                        break
            # Tour du joueur 2 (même commentaires que pour le joueur 1)
                elif turn == 1:
                    await ctx.send(f'{user}: `Attack, Heal, Surrender`')
                    def check(n):
                        return n.content == 'attack' or n.content == 'Attack' or n.content == 'heal' or n.content == 'Heal' or n.content == 'surrender' or n.content == 'Surrender' and n.author == ctx.message.author
                    response = await client.wait_for('message', check=check)
                    if ("attack" in response.content or "Attack" in response.content):
                        if Hp1 > 0:
                            dmg = [0,1,2,3,4,5,6,7,8,9,10,11,12]
                            dmg = (random.choice(dmg))
                            Hp1 = Hp1 - dmg
                            if dmg <= 0:
                                await ctx.send(f"{P1} esquive l'attaque ! Il reste **{Hp1}** points de vie à {P1}.")
                            if dmg >= 8 and dmg <11:
                                await ctx.send(f"{user} assène un **coup critique** de **{dmg}** dégats ! il reste **{Hp1}** points de vie à {P1}.")
                            if dmg == 2:
                                await ctx.send(f"{user} manque de précision et son coup ne fait que **{dmg}** de dégats. Il reste **{Hp1}** points de vie à {P1}.")
                            if dmg == 1:
                                await ctx.send(f"{user} manque de précision et son coup ne fait que **{dmg}** de dégat. Il reste **{Hp1}** points de vie à {P1}.")
                            if dmg >=3 and dmg <=7:
                                await ctx.send(f"{user} inflige **{dmg}** de dégats."f" Il reste **{Hp1}** points de vie à {P1}.")
                            turn = turn - 1
                            if dmg >= 11:
                                await ctx.send(f"{user} assène un **coup critique** de **{dmg}** dégats qui paralyse son adversaire! Il reste **{Hp1}** points de vie à {P1} qui perd un tour.")   
                                turn = 1
                            if Hp1 <= 0:
                                await ctx.send(f"**{user} remporte le match.**")
                                break
                        elif Hp1 <= 0:
                            await ctx.send(f"**{user} remporte le match.**")
                            break
                    if "heal" in response.content or "Heal" in response.content:
                        if Hp2 >= 30 and potionB >= 1:
                            potionB = potionB - 1
                            await ctx.send(f"{user} à déjà **{Hp2}** points de vie, il/elle perd son tour. Il lui reste {potionB} potions.")
                            Hp2 = 30
                            turn = 0
                        if potionB <= 0:
                            await ctx.send(f"{user} n'a plus de potions, il/elle perd son tour.")
                            turn = 0
                        if Hp2 <30 and potionB >0:
                            potion = [3, 4, 5, 6, 7, 8, 9, 10]
                            potion = (random.choice(potion))
                            Hp2 = Hp2 + potion
                            if Hp2 > 30:
                                Hp2 = 30
                            potionB = potionB - 1
                            await ctx.send(f"{user} utilise une **potion** et récupère **{potion}** points de vie. Il lui reste maintenant **{Hp2}** points de vie et {potionB} potions.")
                            
                            turn = 0
                    if "surrender" in response.content or "Surrender" in response.content:
                        await ctx.send(f"{user} abandonne avec **{Hp2}** point de vie restants. {P1} remporte le match avec **{Hp1}** points de vie restants.")
                        Hp1 = Hp1 - Hp1
                        Hp2 = Hp2 - Hp2
                        turn = -1
                        break

client.run("token")