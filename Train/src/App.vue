<script setup>
  import axios from "axios";
  import { reactive } from "vue";
  import { library } from "@fortawesome/fontawesome-svg-core";
  import {
    faChevronUp,
    faChevronDown,
    faQuestionCircle,
  } from "@fortawesome/free-solid-svg-icons";
  import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
  library.add(faChevronUp, faChevronDown, faQuestionCircle);

  const state = reactive({
    guess: "",
    guessedWord: "",
    errorMessage: null,
    isOpen: null,
    isOpenMore: null,
    similarity: null,
    isShown: false,
    isLoading: false,
    isPlaying: false,
    questions: [
      {
        title: "How is the word order definded?",
        text: "The game uses an artificial intelligence algorithm and thousands of texts to calculate the similarity of the words in relation to the word of the day. Not necessarily it is related to the meaning of the words, but to the proximity in which they are used on the internet. For example, if the word of the day were “infinite”, words related to “love” or words related to “universe” might be close to the word of the day because “infinite” is commonly used in those two different contexts. In similar reasoning, if “tv” and “television”, for example, are in very different positions, it means that they are used differently in relation to the word of the day, despite being the same object.",
      },
      {
        title: "How can i ask for a hint?",
        text: "Click on the three dots located on the upper right corner of the screen and select the option “Hint” and it will reveal one word.",
      },
      {
        title:
          "I couldn't figure the word out. Can I see what the word of the day is?",
        text: "In case you don't want to keep trying to guess the word, you have the option to give up. In order to do it, click on the three dots located on the upper right corner of the screen and select the option “Give up”. The word of the day will be displayed on the screen.",
      },
      {
        title: "I want to play more than one game a day, is that possible?",
        text: "Yes. It is possible to play the games of previous days since Contexto launch day or to play a random game. To do so, click on the three dots located on the upper right corner of the screen and select the option “Previous games”. You can choose the game of some specific day or play on random mode.",
      },
      {
        title: "I couldn't play yesterday. Can I still play yesterday's game?",
        text: "Yes, the previous games can be played anytime. To do so, click on the three dots located on the upper right corner of the screen and select the option “Previous games”. You can choose the game of some specific day or play on random mode.",
      },
      {
        title: "I want to play in another language, how can I do that?",
        text: "Click on the three dots located on the upper right corner of the screen and select “Settings” to change the language. The words of the day are not the same in different languages.",
      },
    ],
  });

  const switchAccordion = (idx, isMore) => {
    if (isMore) {
      state.isOpenMore = state.isOpenMore === idx ? null : idx;
    } else {
      state.isOpen = state.isOpen === idx ? null : idx;
    }
  };

  const toggleMore = () => {
    state.isOpen = null;
    state.isOpenMore = null;
    state.isShown = !state.isShown;
  };

  const submitGuess = async () => {
    state.isPlaying = true;
    try {
      state.isLoading = true;
      const response = await axios.post(
        "http://127.0.0.1:8000/api/guessed-word/",
        {
          game_id: 1,
          guess: state.guess,
        }
      );
      state.similarity = response.data.similarity_score;
      state.guessedWord = response.data.guessed_word;
      state.errorMessage = null;
    } catch (error) {
      state.errorMessage = error.response?.data?.error
        ? error.response.data.error
        : "An error occurred. Please try again later.";
    } finally {
      state.isLoading = false;
    }
  };
</script>

<template>
  <div class="min-h-screen bg-slate-900 flex flex-col max-h-fit px-[25%]">
    <div
      class="w-full flex flex-row justify-center items-center my-4 px-10 font-bold"
    >
      <div class="flex-1 inline-flex justify-center items-center text-3xl">
        Context
      </div>
      <div class="inline-flex items-center">Bar</div>
    </div>
    <div class="flex flex-row gap-4 px-3 my-2">
      <div>
        Game:
        <span class="text-lg font-semibold">GameTag</span>
      </div>
      <div>
        Guesses:
        <span class="text-lg font-semibold">Number</span>
      </div>
    </div>
    <div class="my-2">
      <input
        v-model="state.guess"
        type="text"
        name="guess"
        placeholder="Type a word"
        class="bg-slate-700 w-full border-2 border-slate-500 rounded-md text-xl py-2.5 px-5 placeholder:text-xl placeholder:leading-5 hover:border-white focus:border-white"
      />
      <button
        @click="submitGuess"
        class="bg-blue-500 text-white p-2 mt-2 rounded"
      >
        {{ state.isLoading ? "Loading..." : "Submit" }}
      </button>
      <div v-if="state.isPlaying">
        <div v-if="state.errorMessage" class="text-red-500 text-sm mt-2">
          {{ state.errorMessage }}
        </div>
        <div >
          Similarity: {{ state.similarity }}
          <br />
          Guessed Word: {{ state.guessedWord }}
        </div>
      </div>
    </div>
    <div class="bg-slate-800 my-2 py-5 px-7 rounded-md">
      <div class="flex flex-row gap-4 items-center">
        <font-awesome-icon :icon="['fas', 'question-circle']" />
        <p class="text-xl font-bold">How to play</p>
      </div>
      <div class="text-lg">
        <p class="py-1.5">Find the secret word. You have unlimited guesses.</p>
        <p class="py-1.5">
          The words were sorted by an artificial intelligence algorithm
          according to how similar they were to the secret word.
        </p>
        <p class="py-1.5">
          After submitting a word, you will see its position. The secret word is
          number 1.
        </p>
        <p class="py-1.5">
          The algorithm analyzed thousands of texts. It uses the context in
          which words are used to calculate the similarity between them.
        </p>
      </div>
    </div>
    <div class="my-2 px-7">
      <div class="flex flex-row gap-4 items-center">
        <font-awesome-icon :icon="['fas', 'question-circle']" />
        <p class="text-xl font-bold">FAQ</p>
      </div>
      <div id="accordion" class="mb-5">
        <div
          class=""
          v-for="(question, idx) in state.questions.slice(0, 2)"
          :key="idx"
        >
          <h3 class="text-xl font-semibold">
            <button
              type="button"
              @click="switchAccordion(idx, false)"
              class="border-slate-100 text-slate-200 rounded-t-1 flex flex-row justify-between items-center w-full cursor-pointer border-b border-solid p-4 text-left font-semibold"
            >
              <span class="max-w-[375px]">{{ question.title }}</span>
              <font-awesome-icon
                :icon="[
                  'fa',
                  state.isOpen === idx ? 'chevron-up' : 'chevron-down',
                ]"
              />
            </button>
          </h3>
          <div
            class="overflow-hidden transition-all duration-500 ease-in-out"
            :class="{
              'max-h-[250px]': state.isOpen === idx,
              'max-h-0': state.isOpen !== idx,
            }"
          >
            <p class="p-4 text-md">
              {{ question.text }}
            </p>
          </div>
        </div>
      </div>
    </div>
    <div class="my-2 flex justify-center items-center">
      <button
        @click="toggleMore()"
        class="bg-transparent hover:bg-slate-800 p-3 rounded-md text-md font-medium"
      >
        Read more ...
      </button>
    </div>
    <div
      v-if="state.isShown"
      class="absolute my-20 flex justify-center items-center"
    >
      <div class="bg-gray-900 p-5 rounded-3xl">
        <div class="flex flex-row justify-between items-center">
          <div class="flex flex-row gap-4 items-center">
            <font-awesome-icon :icon="['fas', 'question-circle']" />
            <p class="text-xl font-bold">FAQ</p>
          </div>
          <button
            @click="toggleMore()"
            class="bg-transparent hover:bg-slate-800 p-3 rounded-md text-md font-medium"
          >
            Close
          </button>
        </div>
        <div id="accordion-more" class="mb-5">
          <div class="" v-for="(question, idx) in state.questions" :key="idx">
            <h3 class="text-xl font-semibold">
              <button
                type="button"
                @click="switchAccordion(idx, true)"
                class="border-slate-100 text-slate-200 rounded-t-1 flex flex-row justify-between items-center w-full p-4 cursor-pointer border-b border-solid text-left font-semibold"
              >
                <span class="max-w-[425px]">{{ question.title }}</span>
                <font-awesome-icon
                  :icon="[
                    'fa',
                    state.isOpenMore === idx ? 'chevron-up' : 'chevron-down',
                  ]"
                />
              </button>
            </h3>
            <div
              class="overflow-hidden transition-all duration-500 ease-in-out"
              :class="{
                'max-h-[250px]': state.isOpenMore === idx,
                'max-h-0': state.isOpenMore !== idx,
              }"
            >
              <p class="p-4 text-md max-w-[500px]">
                {{ question.text }}
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
