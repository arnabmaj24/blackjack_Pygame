import pygame
import random
import time


width = 800
hieght = 600
screen = pygame.display.set_mode((width, hieght))
pygame.display.set_caption('BlackJack')
pygame.init()
bg = pygame.image.load('bg.jpg')
class Card():
    def __init__(self, value, suit):
        self.value = value
        self.suit = suit

    def show(self):
        if 1 < self.value < 11:
            print("{} of {}".format(self.value, self.suit))
        elif 1 == self.value:
            print("Ace of {}".format(self.suit))
        elif 11 == self.value:
            print("Jack of {}".format(self.suit))
        elif 12 == self.value:
            print("Queen of {}".format(self.suit))
        elif 13 == self.value:
            print("Queen of {}".format(self.suit))

    def get_value(self):
        if 1 < self.value < 11:
            return self.value
        elif self.value == 1:
            return self.value + 10
        elif 11 == self.value:
            return self.value - 1
        elif 12 == self.value:
            return self.value - 2
        elif 13 == self.value:
            return self.value - 3

    def image(self):
        Su = ""
        if self.suit == "Spades":
            Su = "S"
        elif self.suit == "Hearts":
            Su = "H"
        elif self.suit == "Clubs":
            Su = "C"
        elif self.suit == "Diamonds":
            Su = "D"
        if 1 < self.value < 11:
            PNG = str(self.value)+Su+".PNG"
        elif 1 == self.value:
            PNG = "A"+Su+".PNG"
        elif 11 == self.value:
            PNG = "J"+Su+".PNG"
        elif 12 == self.value:
            PNG = "Q"+Su+".PNG"
        elif 13 == self.value:
            PNG = "K" + Su + ".PNG"
        image = pygame.image.load(PNG)
        resized = pygame.transform.scale(image, (90, 140))
        return resized


class Deck():
    def __init__(self):
        self.cards = []
        self.build()

    def build(self):
        for s in ["Spades", "Hearts", "Clubs", "Diamonds"]:
            for v in range(1, 14):
                self.cards.append(Card(v, s))

    def shuffle(self):
        for i in range(len(self.cards) - 1, 0, -1):
            r = random.randint(0, i)
            self.cards[i], self.cards[r] = self.cards[r], self.cards[i]

    def drawCard(self):
        return self.cards.pop()



class Player():
    def __init__(self):
        self.hand = []

    def draw(self, deck):
        self.hand.append(deck.drawCard())
        return self

    def showHand(self):
        for card in self.hand:
            card.show()

    def get_value(self):
        for card in reversed(self.hand):
            return card.get_value()

    def get_image(self):
        for card in reversed(self.hand):
            return card.image()

    def get_a_image(self):
        hand = self.hand
        car = hand[-1]
        return car.image()

class Dealer():
    def __init__(self):
        self.dealHand = []
        self.hidden = []

    def draw(self, deck):
        self.dealHand.append(deck.drawCard())
        return self

    def showDHand(self):
        for card in self.dealHand:
            card.show()

    def Hidden(self, deck):
        self.hidden.append(deck.drawCard())
        return self

    def showHidden(self):
        for card in self.hidden:
            card.show()

    def get_value(self):
        for card in reversed(self.dealHand):
            return card.get_value()

    def get_h_image(self):
        car = self.hidden[0]
        return car.image()

    def get_hidden_value(self):
        for card in reversed(self.hidden):
            return card.get_value()

    def get_a_image(self):
        hand = self.dealHand
        car = hand[-1]
        return car.image()


class Game():
    def __init__(self, pval, dval):
        self.pval = pval
        self.dval = dval
        self.font = pygame.font.Font('freesansbold.ttf', 30)
        self.bigfont = pygame.font.Font('freesansbold.ttf', 40)

    def boot(self, deck, play, deal, gap):
        smallerfont = pygame.font.Font('freesansbold.ttf', 20)
        rules = smallerfont.render("Blackjack with bad logic. All aces are worth 11,", True, (255,255,255))
        rules2 = smallerfont.render("Dealer will take a card at under 17, this still needs improvment",True,(255,255,255))
        screen.blit(rules, (0, 0))
        screen.blit(rules2, (0,25))


        play.draw(deck)
        self.pval += play.get_value()
        screen.blit(play.get_a_image(), (100, 200))
        play.draw(deck)
        screen.blit(play.get_a_image(), (100+gap, 200))
        self.pval += play.get_value()
        deal.draw(deck)
        screen.blit(deal.get_a_image(), (100+gap, 400))
        pygame.draw.rect(screen, (255,0,0), pygame.Rect(45, 245, 50, 50))
        pscore = self.bigfont.render(str(self.pval), True, (255,255,255))
        screen.blit(pscore, (50, 250))
        self.dval += deal.get_value()
        deal.Hidden(deck)
        screen.blit(deal.get_h_image(), (100, 400))
        back = pygame.image.load('blue_back.PNG')
        back1 = pygame.transform.scale(back, (90, 140))
        screen.blit(back1, (100, 400))
        self.dval += deal.get_hidden_value()
        pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(45, 445, 50, 50))
        dscore = self.bigfont.render(str(self.dval-deal.get_hidden_value()), True, (255,255,255))
        screen.blit(dscore, (50, 450))


    def GameLoop(self, deck, play, deal, gap, x, y):
        Looping = True
        while Looping:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    Looping = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        play.draw(deck)
                        self.pval += play.get_value()
                        screen.blit(play.get_a_image(), (100+((x+1)*gap), 200))
                        deal.draw(deck)
                        x += 1
                        screen.blit(deal.get_a_image(), (100+((y+1)*gap), 400))
                        y += 1
                        self.dval += deal.get_value()
                        pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(45, 445, 50, 50))
                        dscore = self.bigfont.render(str(self.dval - deal.get_hidden_value()), True, (255, 255, 255))
                        screen.blit(dscore, (50, 450))
                        pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(45, 245, 50, 50))
                        pscore = self.bigfont.render(str(self.pval), True, (255, 255, 255))
                        screen.blit(pscore, (50, 250))
                        pygame.display.update()


                        if self.pval > 21:
                            screen.blit(deal.get_h_image(), (100, 400))
                            pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(45, 445, 50, 50))
                            dscore = self.bigfont.render(str(self.dval), True, (255, 255, 255))
                            screen.blit(dscore, (50, 450))
                            text = self.bigfont.render("You Busted. You Lose.", True, (255, 255, 255))
                            screen.blit(text, (200, 100))
                            time.sleep(1)
                            Looping = False
                        elif self.pval < 21 and self.dval > 21:
                            screen.blit(deal.get_h_image(), (100, 400))
                            pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(45, 445, 50, 50))
                            dscore = self.bigfont.render(str(self.dval), True, (255, 255, 255))
                            screen.blit(dscore, (50, 450))
                            pygame.display.update()
                            text = self.bigfont.render("Dealer Bust. You win!", True, (255, 255, 255))
                            screen.blit(text, (200, 100))
                            time.sleep(1)
                            Looping = False
                        elif self.pval == 21:
                            screen.blit(deal.get_h_image(), (100, 400))
                            pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(45, 445, 50, 50))
                            dscore = self.bigfont.render(str(self.dval), True, (255, 255, 255))
                            screen.blit(dscore, (50, 450))
                            text = self.font.render("BlackJack! You win", True, (255, 255, 255))
                            screen.blit(text, (200, 100))
                            if self.dval != 21:
                                pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(45, 445, 50, 50))
                                dscore = self.bigfont.render(str(self.dval), True, (255, 255, 255))
                                screen.blit(dscore, (50, 450))
                                text = self.font.render("BlackJack! You win", True, (255, 255, 255))
                                screen.blit(text, (200, 100))
                            elif self.dval == 21:
                                pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(45, 445, 50, 50))
                                dscore = self.bigfont.render(str(self.dval), True, (255, 255, 255))
                                screen.blit(dscore, (50, 450))
                                text = self.font.render("Tie Game.", True, (255, 255, 255))
                                screen.blit(text, (200, 100))
                            Looping = False
                        else:
                            continue

                    if event.key == pygame.K_BACKSPACE:
                        if self.dval < 17:
                            deal.draw(deck)
                            screen.blit(deal.get_a_image(), (100 + ((y + 1) * gap), 400))
                            y += 1
                            self.dval += deal.get_value()
                            screen.blit(deal.get_h_image(), (100, 400))
                            pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(45, 445, 50, 50))
                            dscore = self.bigfont.render(str(self.dval), True, (255, 255, 255))
                            screen.blit(dscore, (50, 450))
                            pygame.display.update()
                        else:
                            screen.blit(deal.get_h_image(), (100, 400))
                            pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(45, 445, 50, 50))
                            dscore = self.bigfont.render(str(self.dval), True, (255, 255, 255))
                            screen.blit(dscore, (50, 450))
                            pygame.display.update()

                        if self.dval > self.pval and self.dval <= 21:
                            text = self.font.render("Dealer has better cards, you Lose.", True, (255, 255, 255))
                            screen.blit(text, (200, 100))
                            pygame.display.update()
                            Looping = False
                        elif self.pval > self.dval or self.dval > 21:
                            text = self.font.render("You have better cards, you Win.", True, (255, 255, 255))
                            screen.blit(text, (200, 100))
                            pygame.display.update()
                            Looping = False


run = True
while run:
    pygame.time.delay(0)
    screen.blit(bg, (0,0))
    pygame.display.update()

    deck = Deck()
    deck.build
    deck.shuffle()
    play = Player()
    deal = Dealer()
    game = Game(0, 0)
    game.boot(deck, play, deal, 120)
    pygame.display.update()
    game.GameLoop(deck, play, deal, 120, 1, 1)
    pygame.display.update()
    time.sleep(1)
    run = False

pygame.quit()
