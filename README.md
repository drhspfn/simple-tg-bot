# simple-tg-bot


# Description
Represents the basis for the bot. 
The bot is written using: `aiogram` `sqlalchemy`. 

# Stored user data
## Local
There is storage of user data in memory. When the bot is closed, it handles saving them, and reading them on startup (If they are there)

The `DataStorage` class in `./util/user_data.py` describes the user data storage. Retrieve, modify, save and read. 


## DB
The database is described by classes, in the file "`./util/base_data.py`".
You can use the [sqlalchemy docs](https://docs.sqlalchemy.org/en/20/) for help

You can use this as a basis:
```python
class Table_News(Base):
    __tablename__ = 'news'
    id = sa.Column(sa.Integer,primary_key=True, autoincrement=True)
    new_name = sa.Column(sa.String)
    new_media_data = sa.Column(sa.Text)
    new_media_caption = sa.Column(sa.Text)
    new_media_button = sa.Column(sa.Text)

    async def get(self):
        try:
            return (
                int(self.id), self.new_name, json.loads(self.new_media_data), 
                self.new_media_caption, json.loads(self.new_media_button)
            )
        except json.decoder.JSONDecodeError:
            return (
                int(self.id), self.new_name, self.new_media_data, 
                self.new_media_caption, self.new_media_button
            )

```
Create a database, put it in the right place and specify the path to it during initialization.

Variables and columns are best pressed the same way.
An example of a table `news` that matches the class `Table_News`:
![example](https://i.imgur.com/52JeAZZ.png)

# Bot initialization example
```python
bot_util = APP("./database.db", './config.json', './util/user_data.json')
bot = Bot(token=bot_util.token(), parse_mode="html", disable_web_page_preview=True, timeout=30)
dp = Dispatcher(bot)
bot_util.set_dp(dp)

```
