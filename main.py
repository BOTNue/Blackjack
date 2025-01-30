import tkinter
from tkinter import messagebox
import random
from PIL import Image, ImageTk
from card import Card




def main():


    def resize_cards(card):
        # Open the image
        card_img = Image.open(card)

        # Resize the image
        card_resize_img = card_img.resize((120,188))

        # Output the card
        global card_image
        card_image = ImageTk.PhotoImage(card_resize_img)

        # return that card
        return card_image

     # Start game/shuffle card stack
    def play():
        global win_status, player_total, dealer_total
        win_status = {"player":"no", "dealer":"no"}
        player_total = 0
        dealer_total = 0
        # Enable buttons when restart button pressed
        hit_button.config(state="normal")
        stand_button.config(state="normal")
        # Clears the game when restart game is pressed
        player_label_1.config(image="")
        player_label_2.config(image="")
        player_label_3.config(image="")
        player_label_4.config(image="")
        player_label_5.config(image="")
        dealer_label_1.config(image="")
        dealer_label_2.config(image="")
        dealer_label_3.config(image="")
        dealer_label_4.config(image="")
        dealer_label_5.config(image="")

        suits = ["diamonds", "clubs", "hearts", "spades"]

        values = range(2, 15)

        # Create a deck of cards
        global deck
        deck = []

        for Card.suit in suits:
            for Card.value in values:
                deck.append(f"{Card.value}_of_{Card.suit}")

        # Create a hand for the player and dealer
        global dealer, player,dealer_score, player_score, dealer_slot, player_slot
        dealer = []
        player = []
        dealer_score = []
        player_score = []
        dealer_slot = 0
        player_slot = 0

        # Deals out two cards to the player and dealer when the game starts
        dealer_hit()
        dealer_hit()

        player_hit()
        player_hit()

    def win(player):
        global player_total, dealer_total
        # Keeps track of total score
        player_total = sum(player_score)
        dealer_total = sum(dealer_score)

        if player == "dealer":
            if dealer_total == 21:
                win_status["dealer"] = "yes"
            elif dealer_total > 21:
                # Checks for ace conversion
                for card_num, card in enumerate(dealer_score):
                    if card == 11:
                        dealer_score[card_num] = 1
                        # Clears dealer total and recalculates total
                        dealer_total = 0
                        for score in dealer_score:
                            dealer_total += score
                        # Check if over 21 total
                        if dealer_total > 21:
                            win_status["dealer"] = "bust"
                else:
                    # Check if the new total is 21 or over 21
                    if dealer_total == 21:
                        win_status["dealer"] = "yes"
                    if dealer_total > 21:
                        win_status["dealer"] = "bust"
                win_status["dealer"] = "bust"

        if player == "player":
            if player_total == 21:
                win_status["player"] = "yes"
            elif player_total > 21:
                # Checks for ace conversion
                for card_num, card in enumerate(player_score):
                    if card == 11:
                        player_score[card_num] = 1

                        # Clears player total and recalculates total 
                        player_total = 0
                        for score in player_score:
                            player_total += score

                        # Check if over 21 total
                        if player_total > 21:
                            win_status["player"] = "bust"
                else:
                    # Check if the new total is 21 or over 21
                    if player_total == 21:
                        win_status["player"] = "yes"
                    if player_total > 21:
                        win_status["player"] = "bust"

        if len(dealer_score) == 2 and len(player_score) == 2:
            # Checks for a tie
            if win_status["dealer"] == "yes" and win_status["player"] == "yes":
                messagebox.showinfo("It's a tie", "Both got blackjack, it's a tie")
                # Disables the hit and stand button when it's a tie
                hit_button.config(state="disabled")
                stand_button.config(state="disabled")
                # Checks for dealer win
            elif win_status["dealer"] == "yes":
                messagebox.showinfo("It's a win", "Dealer got blackjack, dealer wins!")
                # Disables the hit and stand buttton when the dealer gets blackjack
                hit_button.config(state="disabled")
                stand_button.config(state="disabled")
                # Checks for player win
            elif win_status["player"] == "yes":
                messagebox.showinfo("It's a win", "Player got blackjack, player wins!")
                # Disables the hit and stand buttton when the player gets blackjack
                hit_button.config(state="disabled")
                stand_button.config(state="disabled")
        else:
            if win_status["dealer"] == "yes" and win_status["player"] == "yes":
                messagebox.showinfo("It's a tie", f"Both got {player_total}, it's a tie")
                hit_button.config(state="disabled")
                stand_button.config(state="disabled")
            elif win_status["player"] == "yes":
                messagebox.showinfo("It's a win", f"Player wins, player got {player_total}")
                hit_button.config(state="disabled")
                stand_button.config(state="disabled")
        # Checks if player bust 
        if win_status["player"] == "bust":
            messagebox.showinfo("Player bust", f"Player busts, player got {player_total}")
            # Disables the hit and stand buttons when player bust
            hit_button.config(state="disabled")
            stand_button.config(state="disabled")

    def stand():
        global player_total, dealer_total
        # Keeps track of total score
        player_total = sum(player_score)
        dealer_total = sum(dealer_score)
        # Disables the hit and stand buttons
        hit_button.config(state="disabled")
        stand_button.config(state="disabled")

        if dealer_total >= 17:
            # Checks if dealer bust
            if dealer_total > 21:
                messagebox.showinfo("dealer bust", f"dealer busts, dealer got {dealer_total}")
                # Checks if it's a tie
            elif dealer_total == player_total:
                messagebox.showinfo("It's a tie", f"It's a tie, player: {player_total} dealer: {dealer_total}")
                # Checks if dealer has a higher score than player without exceeding 21
            elif dealer_total > player_total:
                messagebox.showinfo("It's a win", f"Dealer wins, dealer got {dealer_total}")
                # Runs if non of the statements above are correct 
            else:
                messagebox.showinfo("It's a win", f"Player wins, player got {player_total}")

        else:
            # Dealer plays hit
            dealer_hit()
            # Evaluates dealer score
            stand()

    def dealer_hit():
        global dealer_slot
        if dealer_slot < 5:
            # Draws a random card from the deck
            card = random.choice(deck)

            # Adds the card to the dealer's hand
            dealer.append(card)

            # Convert card string to integer
            card_convert = int(card.split("_", 1)[0])

            # Ace converts to a score 11 instead of 14
            if card_convert == 14:
                dealer_score.append(11)
                # Faced acrds converts to a score of 10  
            elif card_convert == 13 or card_convert == 12 or card_convert == 11:
                dealer_score.append(10)
            else:
                dealer_score.append(card_convert)

            # Outputs the added cards image to the dealer's label
            global dealer_image_1, dealer_image_2, dealer_image_3, dealer_image_4, dealer_image_5

            if dealer_slot == 0:
                dealer_image_1 = resize_cards(f"image/{card}.png")
                dealer_label_1.config(image=dealer_image_1)
                # Increases amount of cards in dealer hand
                dealer_slot += 1
            elif dealer_slot == 1:
                dealer_image_2 = resize_cards(f"image/{card}.png")
                dealer_label_2.config(image=dealer_image_2)
                # Increases amount of cards in dealer hand
                dealer_slot += 1
            elif dealer_slot == 2:
                dealer_image_3 = resize_cards(f"image/{card}.png")
                dealer_label_3.config(image=dealer_image_3)
                # Increases amount of cards in dealer hand
                dealer_slot += 1
            elif dealer_slot == 3:
                dealer_image_4 = resize_cards(f"image/{card}.png")
                dealer_label_4.config(image=dealer_image_4)
                # Increases amount of cards in dealer hand
                dealer_slot += 1
            elif dealer_slot == 4:
                dealer_image_5 = resize_cards(f"image/{card}.png")
                dealer_label_5.config(image=dealer_image_5)
                # Increases amount of cards in dealer hand
                dealer_slot += 1
            win("dealer")  
    
    
    def player_hit():
        global player_slot
        if player_slot < 5:
            # Draws a random card from the deck
            card = random.choice(deck)
    
            # Adds the card to the players hand
            player.append(card)

            # Convert card string to integer
            card_convert = int(card.split("_", 1)[0])

            if card_convert == 14:
                player_score.append(11)
            elif card_convert == 13 or card_convert == 12 or card_convert == 11:
                player_score.append(10)
            else:
                player_score.append(card_convert)

            # Outputs the added cards image to the players label
            global player_image_1, player_image_2, player_image_3, player_image_4, player_image_5
            
            if player_slot == 0:
                player_image_1 = resize_cards(f"image/{card}.png")
                player_label_1.config(image=player_image_1)
                # Increases amount of cards in player hand
                player_slot += 1
            elif player_slot == 1:
                player_image_2 = resize_cards(f"image/{card}.png")
                player_label_2.config(image=player_image_2)
                # Increases amount of cards in player hand
                player_slot += 1
            elif player_slot == 2:
                player_image_3 = resize_cards(f"image/{card}.png")
                player_label_3.config(image=player_image_3)
                # Increases amount of cards in player hand
                player_slot += 1
            elif player_slot == 3:
                player_image_4 = resize_cards(f"image/{card}.png")
                player_label_4.config(image=player_image_4)
                # Increases amount of cards in player hand
                player_slot += 1
            elif player_slot == 4:
                player_image_5 = resize_cards(f"image/{card}.png")
                player_label_5.config(image=player_image_5)
                # Increases amount of cards in player hand
                player_slot += 1
        win("player")
            
    # Change start game button text
    def change():
        start_game_button.config(text="Restart game")     
    
    # Setup window
    window = tkinter.Tk()
    window.title("Blackjack")
    window.minsize(width=700, height=500)
    window.config(padx=50, pady=50)
    window.configure(background="green")
    # Setup frames
    my_frame = tkinter.Frame(bg="green")
    my_frame.pack(pady=20)

    player_frame = tkinter.LabelFrame(my_frame,text="Player", bd=0)
    dealer_frame = tkinter.LabelFrame(my_frame, text="Dealer", bd=0)
    player_frame.grid(column=1, row=1, padx=20, pady=20)
    dealer_frame.grid(column=1, row=0, padx=20)

    # Labels
    player_label_1 = tkinter.Label(player_frame, text="")
    player_label_2 = tkinter.Label(player_frame, text="")
    player_label_3 = tkinter.Label(player_frame, text="")
    player_label_4 = tkinter.Label(player_frame, text="")
    player_label_5 = tkinter.Label(player_frame, text="")
    dealer_label_1 = tkinter.Label(dealer_frame, text="")
    dealer_label_2 = tkinter.Label(dealer_frame, text="")
    dealer_label_3 = tkinter.Label(dealer_frame, text="")
    dealer_label_4 = tkinter.Label(dealer_frame, text="")
    dealer_label_5 = tkinter.Label(dealer_frame, text="")
    player_label_1.grid(column=0, row=1, padx=20, pady=20)
    player_label_2.grid(column=1, row=1, padx=20, pady=20)
    player_label_3.grid(column=2, row=1, padx=20, pady=20)
    player_label_4.grid(column=3, row=1, padx=20, pady=20)
    player_label_5.grid(column=4, row=1, padx=20, pady=20)
    dealer_label_1.grid(column=0, row=0, padx=20, pady=20)
    dealer_label_2.grid(column=1, row=0, padx=20, pady=20)
    dealer_label_3.grid(column=2, row=0, padx=20, pady=20)
    dealer_label_4.grid(column=3, row=0, padx=20, pady=20)
    dealer_label_5.grid(column=4, row=0, padx=20, pady=20)

    # Setup button
    start_game_button = tkinter.Button(my_frame, text="Start Game", command=lambda: [play(), change()])
    hit_button = tkinter.Button(my_frame, text="Hit", width=5, height=1, command=player_hit)
    stand_button = tkinter.Button(my_frame, text="Stand", width=5, height=1, command=stand)
    start_game_button.grid(column=1, row=2)
    hit_button.grid(column=0, row=3)
    stand_button.grid(column=2, row=3)
    
    # Run the program
    window.mainloop()

if __name__ == "__main__":
    main()