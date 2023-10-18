import turtle, random, time, gc, cProfile, math

from playsound import playsound

screen = turtle.Screen()
turtle.tracer(False)
attempts = 10

# feedback = turtle.Turtle()
# feedback.penup()
# feedback.hideturtle()

def add_lb(toWrite):
    filee = open("leaderboard.txt", "r+")
    lines = filee.read().splitlines()
    # user + " | Score: " + str(scoreCounter) + " | Attempts: " + str(attempts)
    score = int(toWrite.split(" | ")[1].split(" ")[1])
    # Sort all scores in file and insert new score if it is higher than the others
    if len(lines) > 1:

        for person in lines:
            personsscore = int(person.split(" | ")[1].split(" ")[1])
            if score > personsscore:
                lines.insert(lines.index(person), toWrite)
                break
            elif toWrite not in lines:
                lines.append(toWrite)

    else:
        lines.append(toWrite)

    # Remove last score if there are more than 5 scores
    if len(lines) > 4:
        lines.pop()


    # Write all scores to file
    filee.seek(0)
    filee.truncate()
    filee.write("\n".join(lines))    

def read_lb():
    return open("leaderboard.txt", "r+").read().strip()

def game():
    global attemptCounter
    global attempts
    global scoreCounter
    global hits
    global misses
    global lastx
    global lasty
    global scoreCounter

    gc.collect()

    attemptCounter = 0
    scoreCounter = 0

    hits = 0
    misses = 0 

    lastx = 0
    lasty = 0

    dots = []

    SCREEN_WIDTH = turtle.window_width()
    SCREEN_HEIGHT = turtle.window_height()

    print(SCREEN_WIDTH, SCREEN_HEIGHT)
    # hitmarker=turtle.Turtle()
    # hitmarker.penup()
    # hitmarker.shape("square")
    # hitmarker.hideturtle()
    # badmarker=turtle.Turtle()
    # badmarker.penup()
    # badmarker.shape("triangle")
    # badmarker.hideturtle()
    screen.bgpic("images/background.gif")
    turtle.addshape("images/fish.gif")
    #feedback.goto(0,(SCREEN_HEIGHT/2) - 20)


    def get_time():
        return round(time.time() * 1000)

    #print(SCREEN_WIDTH, SCREEN_HEIGHT)

    def generate_dot():
        print("Generating dot...")
        global before
        dot = turtle.Turtle()
        dot.hideturtle()
        dot.shape("images/fish.gif")

        dot.shapesize(2)
        dot.penup()
        time.sleep(1)
        print(SCREEN_WIDTH, SCREEN_HEIGHT)
        dot.goto(random.randint(-(SCREEN_WIDTH/2), (SCREEN_WIDTH/2)), random.randint(-(SCREEN_HEIGHT/2), (SCREEN_HEIGHT/2)))
        # hitmarker.goto(dot.pos())
        # badmarker.goto(dot.pos())
        print("pos", dot.pos())
        dots.append(dot)
        # feedback.clear()
        dot.showturtle()
        turtle.update()
        before = get_time()


    def handle_click(x,y):
        global attemptCounter        
        if not attemptCounter < attempts:
            return game_over()

        print(dots)
        dot = dots[0]

        
        if dot.distance(x,y) < dot.shapesize()[0] * 10.75:
            handle_success()
        else:
            handle_fail()

        attemptCounter += 1

    def score(hit):
        global hits
        global misses
        if hit:
            print("Hit!")
            hits += 1
        else:   
            print("Miss!")   
            misses += 1

    def scoretotal(x2,y2,difference,dotsize):
        global attemptCounter
        global hits
        global misses
        global lastx
        global lasty
        global scoreCounter
        factor_distance = math.sqrt((x2 - lastx)**2 + (y2 - lasty)**2)
        scoreCounter += round((hits/attempts)*(factor_distance/(difference/100))*dotsize)
        print(scoreCounter)        

    def handle_success():
        toRemove = dots.pop()
        toRemove.hideturtle()

        #hitmarker.showturtle()
        #feedback.write("Hit!", align="center", font=("Arial", 16, "normal"))
        #playsound("sound/hit.wav")
        turtle.update()
        time.sleep(0.1)
        #hitmarker.hideturtle()
        turtle.update()

        after = get_time()

        difference = after - before

        score(True)

        scoretotal(toRemove.xcor(), toRemove.ycor(), difference, toRemove.shapesize()[0] * 10)

        generate_dot()


    def handle_fail():

        toRemove = dots.pop()
        toRemove.hideturtle()
        # badmarker.showturtle()
        # feedback.write("Miss!", align="center", font=("Arial", 16, "normal"))
        turtle.update()
        time.sleep(0.1)
        # badmarker.hideturtle()
        turtle.update()
        score(False)

        generate_dot()

    def game_over():
        global user
        screen.clear()

        # Display user score
        scoreTurtle = turtle.Turtle()
        scoreTurtle.hideturtle()
        scoreTurtle.up()
        scoreTurtle.goto(0, 0)
        scoreTurtle.write("Score: " + str(scoreCounter), align="center", font=("Arial", 32, "normal"))

        # Count down from 3
        countdown = turtle.Turtle()
        countdown.hideturtle()
        countdown.up()
        countdown.goto(0, -50)
        countdown.write("3", align="center", font=("Arial", 32, "normal"))
        turtle.update()
        time.sleep(1)
        countdown.clear()
        countdown.write("2", align="center", font=("Arial", 32, "normal"))
        turtle.update()
        time.sleep(1)
        countdown.clear()
        countdown.write("1", align="center", font=("Arial", 32, "normal"))
        turtle.update()
        time.sleep(1)
        countdown.clear()

        add_lb(user + " | Score: " + str(scoreCounter) + " | Attempts: " + str(attempts))

        screen.clear()

        main_menu()

    generate_dot()
    screen.onclick(handle_click)
    turtle.update()

    screen.mainloop()


def show_leaderboard():
    def handle_action(x,y):
        # Check if user clicked on the back button
        if -100 <= x <= 100 and -213 <= y <= -187:
            # Go back to main menu
            print("Going back to main menu...")
            screen.clear()
            main_menu()

    # Clear the screen
    screen.clear()
    screen.bgpic("images/background.gif")
    print("got here")
    contents = read_lb()
    print(contents)
    leaderboardTurtle = turtle.Turtle()
    leaderboardTurtle.hideturtle()
    leaderboardTurtle.up()
    leaderboardTurtle.goto(0, 200)
    leaderboardTurtle.write(contents, align="center", font=("Arial", 16, "normal"))

    exit_game_button = turtle.Turtle()
    exit_game_button.hideturtle()
    exit_game_button.shape("square")
    exit_game_button.color("red")
    exit_game_button.shapesize(2, 10)
    exit_game_button.up()
    exit_game_button.goto(0, -200)
    exit_game_button.stamp()
    exit_game_button.goto(0, -213)
    exit_game_button.color("white")
    exit_game_button.write("Back", align="center", font=("Arial", 16, "normal"))

    screen.onscreenclick(handle_action)

    turtle.update()

def handle_action(x,y):
    global attempts
    window_height = turtle.window_height()
    print("checking")
    # Check if the user clicked on the start game button
    if -100 <= x <= 100 and 25 <= y <= 75:
        print("Starting game...")
        screen.clear()
        game()

    # Check if the user clicked on the view leaderboard button
    elif -100 <= x <= 100 and -25 <= y <= 25:
        print("Viewing leaderboard...")
        screen.clear()
        show_leaderboard()
        
    # Check if the user clicked on the exit game button
    elif -100 <= x <= 100 and -75 <= y <= -25:
        print("Exiting game...")
        screen.bye()
        
    # Check if the user clicked on the + button
    elif 25 <= x <= 80 and -160 <= y <= -115:
        print("adding")
        attempts += 1
        # Rewrite the number of attempts
        number_of_attempts.clear()
        number_of_attempts.goto(0, -145)
        number_of_attempts.write(str(attempts), align="center", font=("Arial", 16, "normal"))
        print("Number of attempts: " + str(attempts))
        return
    
    # Check if the user clicked on the - button
    elif -70 <= x <= -30 and -160 <= y <= -115:
        print("subtracting")
        if attempts > 1:
            attempts -= 1
            # Rewrite the number of attempts
            number_of_attempts.clear()
            number_of_attempts.goto(0, -145)
            number_of_attempts.write(str(attempts), align="center", font=("Arial", 16, "normal"))
            print("Number of attempts: " + str(attempts))
        return
        



def main_menu():
    # Clear the screen
    
    global attempts
    global number_of_attempts
    screen.bgpic("images/background.gif")
    window_height = turtle.window_height()

    # Game title
    title = turtle.Turtle()
    title.hideturtle()
    title.up()
    title.goto(0, window_height/2 - 150)
    title.write("Reaction Time Game", align="center", font=("Arial", 32, "normal"))

    # Welcome user
    welcome = turtle.Turtle()
    welcome.hideturtle()
    welcome.up()
    welcome.goto(0, window_height/2 - 200)
    welcome.write("Welcome, " + user + "!", align="center", font=("Arial", 16, "normal"))

    # Main menu with buttons to start the game, view the leaderboard, and exit the game
    # Start game button``
    start_game_button = turtle.Turtle()
    start_game_button.hideturtle()
    start_game_button.shape("square")
    start_game_button.color("green")
    start_game_button.shapesize(2, 10)
    start_game_button.up()
    start_game_button.goto(0, 50)
    start_game_button.stamp()
    start_game_button.goto(0, 37)
    start_game_button.color("white")
    start_game_button.write("Start Game", align="center", font=("Arial", 16, "normal"))

    # View leaderboard button
    view_leaderboard_button = turtle.Turtle()
    view_leaderboard_button.hideturtle()
    view_leaderboard_button.shape("square")
    view_leaderboard_button.color("blue")
    view_leaderboard_button.shapesize(2, 10)
    view_leaderboard_button.up()
    view_leaderboard_button.goto(0, 0)
    view_leaderboard_button.stamp()
    view_leaderboard_button.goto(0, -10)
    view_leaderboard_button.color("white")
    view_leaderboard_button.write("View Leaderboard", align="center", font=("Arial", 16, "normal"))

    # Exit game button
    exit_game_button = turtle.Turtle()
    exit_game_button.hideturtle()
    exit_game_button.shape("square")
    exit_game_button.color("red")
    exit_game_button.shapesize(2, 10)
    exit_game_button.up()
    exit_game_button.goto(0, -50)
    exit_game_button.stamp()
    exit_game_button.goto(0, -63)
    exit_game_button.color("white")
    exit_game_button.write("Exit Game", align="center", font=("Arial", 16, "normal"))

    # Credits at the bottom
    credits = turtle.Turtle()
    credits.hideturtle()
    credits.up()
    credits.goto(0, -310)
    credits.write("Credits: Arshan, Ethan, Hope", align="center", font=("Arial", 16, "normal"))

    # In bottom left corner have + and - buttons to change the number of attempts
    # + button
    plus_button = turtle.Turtle()
    plus_button.hideturtle()
    plus_button.shape("square")
    plus_button.color("green")
    plus_button.shapesize(2, 2)
    plus_button.up()
    plus_button.goto(50, -135)
    plus_button.stamp()
    plus_button.goto(50, -150)
    plus_button.color("white")
    plus_button.write("+", align="center", font=("Arial", 20, "normal"))

    # - button
    minus_button = turtle.Turtle()
    minus_button.hideturtle()
    minus_button.shape("square")
    minus_button.color("red")
    minus_button.shapesize(2, 2)
    minus_button.up()
    minus_button.goto(-50, -135)
    minus_button.stamp()
    minus_button.goto(-50, -150)
    minus_button.color("white")
    minus_button.write("-", align="center", font=("Arial", 20, "normal"))

    # Put number of attempts in between the + and - buttons
    number_of_attempts = turtle.Turtle()
    number_of_attempts.hideturtle()
    number_of_attempts.up()
    number_of_attempts.goto(0, -145)
    number_of_attempts.write(str(attempts), align="center", font=("Arial", 16, "normal"))


    # Number of attempts
    attemptsWriter = turtle.Turtle()
    attemptsWriter.hideturtle()
    attemptsWriter.up()
    attemptsWriter.goto(0, -110)
    attemptsWriter.write("Attempts", align="center", font=("Arial", 16, "normal"))


    screen.onscreenclick(handle_action)

    turtle.update()

    screen.mainloop()
    print("a")

# Get user's name using turtle's textinput function
user = turtle.textinput("Reaction Time Game", "What is your name?")

#cProfile.run('main_menu()') Performance monitoring
main_menu()