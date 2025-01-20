import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import mysql.connector
from mysql.connector import Error

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix='!', intents=intents)

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'discord_keys'
}

def init_db():
    conn = None
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password=''
        )
        cursor = conn.cursor()
        
        cursor.execute("CREATE DATABASE IF NOT EXISTS discord_keys")
        cursor.execute("USE discord_keys")
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS license_keys (
                key_id VARCHAR(255) PRIMARY KEY,
                claimed BOOLEAN DEFAULT FALSE
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS claims (
                user_id BIGINT PRIMARY KEY,
                key_id VARCHAR(255),
                claim_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (key_id) REFERENCES license_keys(key_id)
            )
        """)
        
        conn.commit()
        print("Database initialized successfully")
        
    except Error as e:
        print(f"Error initializing database: {e}")
    finally:
        if conn is not None and conn.is_connected():
            cursor.close()
            conn.close()

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    init_db()

@bot.command(name='key')
async def get_key(ctx):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute("SELECT key_id FROM license_keys WHERE claimed = FALSE LIMIT 1")
        result = cursor.fetchone()
        
        if result:
            key = result['key_id']
            
            cursor.execute("UPDATE license_keys SET claimed = TRUE WHERE key_id = %s", (key,))
            cursor.execute("INSERT INTO claims (user_id, key_id) VALUES (%s, %s)", 
                         (ctx.author.id, key))
            conn.commit()
            
            await ctx.send(f'Here is your key: `{key}`', ephemeral=True)
        else:
            await ctx.send('Sorry, no keys are available at the moment.', ephemeral=True)
            
    except Error as e:
        print(f"Database error: {e}")
        await ctx.send('An error occurred while processing your request.', ephemeral=True)
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

@bot.command(name='addkey')
@commands.has_permissions(administrator=True)
async def add_key(ctx, key: str):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        
        cursor.execute("INSERT INTO license_keys (key_id) VALUES (%s)", (key,))
        conn.commit()
        await ctx.send(f'Key added successfully!', ephemeral=True)
        
    except Error as e:
        if e.errno == 1062:
            await ctx.send('This key already exists in the database.', ephemeral=True)
        else:
            print(f"Database error: {e}")
            await ctx.send('An error occurred while adding the key.', ephemeral=True)
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

bot.run(os.getenv('DISCORD_TOKEN'))
