from data_low import data
import random


def get_random_account():
    """Creates a random account from the given data"""
    return random.choice(data)
    

def format_account(account):
    """Formating the account by: Name, Description and Country.
    The Follower count is left out because we will use it later on as a variable"""
    name = account["name"]
    description = account["description"]
    country = account["country"]
    # count = account["follower_count"]

    # print(f'{name}: {account[follower_count]}')

    return f"{name} from {country} a {description}"


def check_answer(guess, celebrity_1, celebrity_2):
    """Checks which celebrity has more followers"""
    if celebrity_1 >= celebrity_2:
        return guess == "a"
    elif celebrity_2 >= celebrity_1:
        return guess == "b"


def game():
    score = 0
    game_continue = True
    account_1 = get_random_account()
    account_2 = get_random_account()

    while game_continue:
        account_1 = account_2
        account_2 = get_random_account()

        while account_1 == account_2:
            account_2 = get_random_account()


        print(f"Compare A: {format_account(account_1)}.")
        print("vs")
        print(f"Against B: {format_account(account_2)}.")

        guess = input('Which celebrity has more followers on IG?? A/B ').lower()
        account_1_count = account_1["follower_count"] # here is when we access the follower count
        account_2_count = account_2["follower_count"]

        winner = check_answer(guess, account_1_count, account_2_count)

        if winner:
            score += 1
            print(f'Correct, your score is {score}.')
        else:
            game_continue = False
            print(f'Incorrect, your score is {score}')
            question = input('Play Again??? Y/N ').capitalize()

            if question == "Y":
                game()
            else:
                print('Farewell!!!')


game()



    


    

    




    # {
    #     'name': 'Instagram',
    #     'follower_count': 346,
    #     'description': 'Social media platform',
    #     'country': 'United States'
    # }

