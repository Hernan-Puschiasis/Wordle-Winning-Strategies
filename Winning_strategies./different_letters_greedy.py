def calculate_letter_frequency(words):
    number_of_letters = 5 * len(words)
    letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
               'N', 'Ñ', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    letter_appeareance = {}
    letter_probability = {}
    for letter in letters:
        letter_appeareance[letter.lower()] = 0

    for word in words:
        for letter in word:
            letter_appeareance[letter] += 1

    for letter in letters:
        letter_probability[letter.lower()] = round(
            letter_appeareance[letter.lower()]/number_of_letters, 4)

    return letter_probability


def words_score(words, letter_frequency):
    words_score = {}
    for word in words:
        try:
            words_score[word] = 0
            for letter in word:
                if word.count(letter) >= 2:
                    words_score[word] += letter_frequency[letter] - 0.06
                else:
                    words_score[word] += letter_frequency[letter]
        except KeyError:
            pass
    return words_score


def get_initial_words():
    words = []
    f = open("words.txt", "r")
    for line in f:
        words.append(line[:-1])
    return words


def has_exact_position(word, guessed):
    for letter in guessed:
        if letter != "":
            if letter == word[guessed.index(letter)]:
                pass
            else:
                return False
    return True


def has_yellow_positions(word, yellow):  # corro [['r'], [], [], ['r'], []]
    for i in range(len(word)):
        if word[i] in yellow[i]:
            return True
    return False


def has_eliminated_letters(word, eliminated):
    for letter in word:
        if letter in eliminated:
            return True
    return False


def has_letters(word, letters):
    for letter in letters:
        if letter not in word:
            return False
    return True


if __name__ == "__main__":
    initial_words = get_initial_words()
    words = get_initial_words()
    first_letter_frequency = calculate_letter_frequency(words)
    new_words = []
    words_for_variety = []
    is_correct = False
    round_counter = 1
    already_guessed_words = []
    eliminated_letters = set({})
    guessed_letters = ["", "", "", "", ""]
    must_be_letters = set({})
    cant_be_there = [[], [], [], [], []]
    already_used_letters = set({})
    while not is_correct:
        #letter_frequency = calculate_letter_frequency(words)
        all_words_score = words_score(words, first_letter_frequency)
        best_word = max(all_words_score, key=all_words_score.get)
        if round_counter <= 3 and round_counter >= 2:
            round_counter += 1
            words_for_variety = []
            is_new_variant_counter = 0
            for word in initial_words:
                for letter in word:
                    if word.count(letter) <= 1 and (letter not in already_used_letters) and (word not in already_guessed_words):
                        is_new_variant_counter += 1
                if is_new_variant_counter == 5:
                    words_for_variety.append(word)
                is_new_variant_counter = 0
            if len(words_for_variety) < 1:
                print(best_word)
                already_guessed_words.append(best_word)

            else:
                word_scores = words_score(
                    words_for_variety, first_letter_frequency)
                best_variety_word = max(word_scores, key=word_scores.get)
                for letter in best_variety_word:
                    already_used_letters.add(letter)
                print(best_variety_word)
                print(already_used_letters)
                already_guessed_words.append(best_variety_word)
                best_word = best_variety_word
        else:
            round_counter += 1
            print(best_word)
            already_guessed_words.append(best_word)
            for letter in best_word:
                already_used_letters.add(letter)
        colours = input("Write the colors, example: GGYBB: ")
        if colours != "GGGGG":
            for i in range(len(colours)):
                if colours[i] == "B":
                    try:
                        eliminated_letters.add(best_word[i])
                    except Exception:
                        pass
                elif colours[i] == "G":
                    guessed_letters[i] = best_word[i]
                    try:
                        must_be_letters.add(best_word[i])
                    except Exception:
                        pass
                else:
                    cant_be_there[i].append(best_word[i])
                    try:
                        must_be_letters.add(best_word[i])
                    except Exception:
                        pass
            new_words = []
            for word in words:
                if (has_exact_position(word, guessed_letters)) and (not has_eliminated_letters(word, eliminated_letters)) and (not has_yellow_positions(word, cant_be_there)) and (has_letters(word, must_be_letters)):
                    if word not in already_guessed_words:
                        new_words.append(word)
            words = new_words
        else:
            is_correct = True
