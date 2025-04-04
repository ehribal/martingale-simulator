# import streamlit as st

# st.title("🎈 My new app")
# st.write(
#     "Let's start building! For help and inspiration, head over to [docs.streamlit.io](https://docs.streamlit.io/)."
# )


import streamlit as st
import numpy as np
from random import randrange

def run_simulation(cash_out, max_loss, initial_bet, multiplier_after_loss, multiplier_after_win):
    iterations = 100000
    win_cash = []
    loss_cash = []
    for _ in range(iterations):
        my_cash = 0
        previous_bet = 0
        last_outcome = -1
        total_rolls = 0
        
        while my_cash < cash_out and my_cash > max_loss and total_rolls < 100:
            if last_outcome == -1:
                bet = initial_bet
            elif last_outcome == 0:
                bet = previous_bet * multiplier_after_loss
            elif last_outcome == 1:
                bet = my_cash * multiplier_after_win

            roll = randrange(1, 40)
            if roll <= 18:
                my_cash += bet
                last_outcome = 1
            else:
                my_cash -= bet
                last_outcome = 0

            previous_bet = bet
            total_rolls += 1

        if my_cash > 0:
            win_cash.append(my_cash)
        elif my_cash < 0:
            loss_cash.append(my_cash)

    return win_cash, loss_cash

# Streamlit UI
st.title("Roulette Simulation")

cash_out = st.number_input("Cash Out Amount", value=100)
max_loss = st.number_input("Max Loss", value=-160)
initial_bet = st.number_input("Initial Bet", value=10)
multiplier_after_loss = st.number_input("If you lose a hand, multiply previous bet by ___ for the next bet:", value=2.0)
multiplier_after_win = st.number_input("If you win a hand, multiply previous bet by ___ for the next bet:", value=.5)
#iterations = st.number_input("Iterations", value=1000)

if st.button("Run Simulation"):
    if initial_bet < 10:
        st.write("Table minimums at a casino def won't be less than $10 :)")
    
    else:
        win_stats, loss_stats = run_simulation(cash_out, max_loss, initial_bet, multiplier_after_loss, multiplier_after_win)
        win_percent = len(win_stats) / 100000
        win_avg = np.average(win_stats)
        loss_avg = np.average(loss_stats)
        ev = (win_percent * win_avg) + ( (1-win_percent) * loss_avg )
        st.write(f"Percentage of Wins: {win_percent}")
        st.write(f"Avg Return from Wins: {win_avg}")
        st.write(f"Avg Return from Losses: {loss_avg}")
        st.write(f"Expected Value: {ev}")