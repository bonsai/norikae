export interface QuizItem {
  id: string;
  text: string;
  order: number;
}

export interface QuizQuestion {
  id: number;
  question: string;
  items: QuizItem[];
  hint?: string;
}

export interface QuizState {
  currentQuestionIndex: number;
  score: number;
  answers: Record<number, string[]>;
  isAnswered: boolean;
  isCorrect: boolean;
  gameComplete: boolean;
}
