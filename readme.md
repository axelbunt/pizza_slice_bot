# Pizza Slice Bot 🍕

## Project description

*Pizza Slice Bot* is a telegram bot designed specifically for pizzeria to facilitate the pizza ordering process for customers. The bot provides a user-friendly interface for getting acquainted with the menu, choosing dishes and paying for an order directly in the Telegram application.

## Getting started with the project

Clone project:

```shell
git init

git clone ...
```

You should create `.env` file and write in it:

```.env
BOT_TOKEN={your bot token}
PAYMENT_TOKEN={your bot payment token}
...
```

See `.env.template` for more variables to write in `.env`...)

Substitution of a value from a virtual environment occurs in file `constants.py`.

Initialize venv and run project in dev-mode:

```shell
python -m venv venv
venv/Scripts/activate

pip install -r requirements/dev.txt

python main.py
```

Another way to activate venv (for Linux/MacOS):

```shell
source venv/bin/activate
```

This will run bot in LongPolling mode.

---

Installing different dependencies for production and developing:
```shell
# prod:
    pip install -r requirements/prod.txt

# dev:
    pip install -r requirements/dev.txt
```

---

## Functionality

1. **Menu of commands**  
Clients can interact with the bot using various commands, such as:
    - `/start` to get started,
    - `/help` to get descriptions of bot commands,
    - `/menu` to get pizzeria menu,
    - `/location` to get location of nearest pizzeria,
    - `/hours` to get pizzeria working hours.

2. **Interactive menu**  
Users can view menu with different types of pizza. Each menu item is provided with a description and price.

3. **Choice of pizzas**  
The ability to select dishes from the menu using the inline buttons. Customers can add and remove items from the cart, see the total cost of the order.

4. **Payment of the order**  
Integration with Stripe payment system to ensure safe and convenient payment of the order. Customers can choose a convenient payment method, such as credit card or electronic payments.

This project will allow the pizzeria to improve customer service by making the ordering process more convenient and efficient through the popular messenger application.

## It's demo time!

Bot description:

![Bot description](/assets/images/demo_screenshots/1.jpg)

Menu of commands:

![Menu of commands](/assets/images/demo_screenshots/2.jpg)

Some commands:

![Some commands](/assets/images/demo_screenshots/3.jpg)

Menu and invoice for payment:

![Menu and invoice for payment](/assets/images/demo_screenshots/4.jpg)