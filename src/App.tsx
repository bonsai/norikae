import { useState, useCallback } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { QuizGame } from '@/components/QuizGame';
import { StartScreen } from '@/components/StartScreen';
import { ResultScreen } from '@/components/ResultScreen';
import type { QuizQuestion, QuizState } from '@/types/quiz';
import devices from '@/data/device.json';
import { DeviceCard } from '@/components/DeviceCard';

// Helper function to parse string values into a comparable number
const parseUnitValue = (value: string): number => {
  const cleanedValue = value.replace(/≈|¥|,/g, '');
  const match = cleanedValue.match(/([\d.]+)\s*(K|M|G)?(B|Hz)?/i);
  if (!match) return 0;

  let num = parseFloat(match[1]);
  const unit = match[2]?.toUpperCase();

  if (unit === 'K') num *= 1e3;
  if (unit === 'M') num *= 1e6;
  if (unit === 'G') num *= 1e9;
  
  return num;
};

// Generic function to create a quiz question from device data
const createQuizFromDevices = (
  key: keyof typeof devices[0],
  question: string,
  hint: string,
  ascending = true
): QuizQuestion => {
  const items = devices
    .map(device => ({
      id: `device-${device.device.replace(/\s/g, '-')}-${key}`,
      text: `${device.device} (${device[key]})`,
      value: parseUnitValue(String(device[key])),
    }))
    .sort((a, b) => ascending ? a.value - b.value : b.value - a.value)
    .map((item, index) => ({
      ...item,
      order: index + 1,
    }))
    .sort(() => Math.random() - 0.5);

  return { id: Math.random(), question, hint, items };
};

// Create multiple quiz questions
const quizQuestions: QuizQuestion[] = [
  createQuizFromDevices('bit_width', '💻 CPUビット幅が小さい順に並べてね！', '8ビットから64ビットまで、歴史を遡ろう'),
  createQuizFromDevices('core_count', '🧠 CPUコア数が多い順に並べてね！', '多いほどたくさんの処理が同時にできるよ', false),
  createQuizFromDevices('max_clock', '⚡️ クロック周波数が高い順に並べてね！', 'GHzはMHzの1000倍だよ', false),
  createQuizFromDevices('ram', '💾 RAM容量が多い順に並べてね！', 'GBはMBの1000倍、MBはKBの1000倍だよ', false),
  createQuizFromDevices('price_yen_2026', '💰 価格が安い順に並べてね！', '2026年時点の参考価格だよ'),
];

function App() {
  const [gameState, setGameState] = useState<'start' | 'playing' | 'result'>('start');
  const [quizState, setQuizState] = useState<QuizState>({
    currentQuestionIndex: 0,
    score: 0,
    answers: {},
    isAnswered: false,
    isCorrect: false,
    gameComplete: false,
  });

  const handleStart = useCallback(() => {
    setGameState('playing');
    setQuizState({
      currentQuestionIndex: 0,
      score: 0,
      answers: {},
      isAnswered: false,
      isCorrect: false,
      gameComplete: false,
    });
  }, []);

  const handleAnswer = useCallback((isCorrect: boolean) => {
    setQuizState((prev) => ({
      ...prev,
      score: isCorrect ? prev.score + 1 : prev.score,
      isAnswered: true,
      isCorrect,
    }));
  }, []);

  const handleNext = useCallback(() => {
    setQuizState((prev) => {
      const nextIndex = prev.currentQuestionIndex + 1;
      if (nextIndex >= quizQuestions.length) {
        return {
          ...prev,
          gameComplete: true,
        };
      }
      return {
        ...prev,
        currentQuestionIndex: nextIndex,
        isAnswered: false,
        isCorrect: false,
      };
    });
  }, []);

  // Check if game is complete
  if (quizState.gameComplete && gameState === 'playing') {
    setGameState('result');
  }

  const currentQuestion = quizQuestions[quizState.currentQuestionIndex];

  return (
    <div className="min-h-screen bg-slate-950 relative overflow-hidden">
      {/* Animated Background */}
      <div className="fixed inset-0 pointer-events-none">
        {/* Gradient Orbs */}
        <motion.div
          animate={{
            x: [0, 100, 0],
            y: [0, -50, 0],
          }}
          transition={{
            duration: 20,
            repeat: Infinity,
            ease: 'linear',
          }}
          className="absolute top-20 left-10 w-96 h-96 rounded-full
                     bg-gradient-to-br from-cyan-500/20 to-blue-500/20
                     blur-[100px]"
        />
        <motion.div
          animate={{
            x: [0, -80, 0],
            y: [0, 80, 0],
          }}
          transition={{
            duration: 15,
            repeat: Infinity,
            ease: 'linear',
          }}
          className="absolute bottom-20 right-10 w-80 h-80 rounded-full
                     bg-gradient-to-br from-fuchsia-500/20 to-purple-500/20
                     blur-[100px]"
        />
        <motion.div
          animate={{
            x: [0, 60, 0],
            y: [0, 60, 0],
          }}
          transition={{
            duration: 18,
            repeat: Infinity,
            ease: 'linear',
          }}
          className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 
                     w-72 h-72 rounded-full
                     bg-gradient-to-br from-yellow-500/10 to-amber-500/10
                     blur-[100px]"
        />

        {/* Grid Pattern */}
        <div 
          className="absolute inset-0 opacity-[0.03]"
          style={{
            backgroundImage: `
              linear-gradient(rgba(255,255,255,0.1) 1px, transparent 1px),
              linear-gradient(90deg, rgba(255,255,255,0.1) 1px, transparent 1px)
            `,
            backgroundSize: '50px 50px',
          }}
        />

        {/* Floating Particles */}
        {[...Array(20)].map((_, i) => (
          <motion.div
            key={i}
            className="absolute w-1 h-1 rounded-full bg-white/30"
            style={{
              left: `${Math.random() * 100}%`,
              top: `${Math.random() * 100}%`,
            }}
            animate={{
              y: [0, -30, 0],
              opacity: [0.3, 0.8, 0.3],
            }}
            transition={{
              duration: 3 + Math.random() * 2,
              repeat: Infinity,
              delay: Math.random() * 2,
            }}
          />
        ))}
      </div>

      {/* Main Content */}
      <div className="relative z-10 min-h-screen flex flex-col items-center justify-center p-4">
        {/* Header */}
        <motion.header
          initial={{ y: -50, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          className="fixed top-0 left-0 right-0 p-4 z-50"
        >
          <div className="max-w-4xl mx-auto flex items-center justify-between">
            <motion.div 
              className="flex items-center gap-2"
              whileHover={{ scale: 1.05 }}
            >
              <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-cyan-400 via-fuchsia-400 to-yellow-400
                              flex items-center justify-center shadow-lg"
              >
                <span className="text-white font-black text-lg">DD</span>
              </div>
              <span className="text-white font-bold text-lg hidden sm:block">
                ソートクイズ
              </span>
            </motion.div>
            
            {gameState === 'playing' && (
              <motion.div
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                className="flex items-center gap-3 px-4 py-2 rounded-full
                           bg-slate-800/80 backdrop-blur-md border border-slate-700"
              >
                <span className="text-slate-400 text-sm">スコア</span>
                <span className="text-fuchsia-400 font-bold text-xl">
                  {quizState.score}
                </span>
              </motion.div>
            )}
          </div>
        </motion.header>

        {/* Game Content */}
        <main className="w-full max-w-4xl mx-auto pt-20">
          <AnimatePresence mode="wait">
            {gameState === 'start' && (
              <motion.div
                key="start"
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                exit={{ opacity: 0, scale: 0.9 }}
                transition={{ duration: 0.3 }}
              >
                <StartScreen onStart={handleStart} />
              </motion.div>
            )}

            {gameState === 'playing' && currentQuestion && (
              <motion.div
                key="game"
                initial={{ opacity: 0, x: 50 }}
                animate={{ opacity: 1, x: 0 }}
                exit={{ opacity: 0, x: -50 }}
                transition={{ duration: 0.3 }}
              >
                <QuizGame
                  question={currentQuestion.question}
                  hint={currentQuestion.hint}
                  items={currentQuestion.items}
                  questionNumber={quizState.currentQuestionIndex + 1}
                  totalQuestions={quizQuestions.length}
                  score={quizState.score}
                  onAnswer={handleAnswer}
                  onNext={handleNext}
                />
              </motion.div>
            )}

            {gameState === 'result' && (
              <motion.div
                key="result"
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                exit={{ opacity: 0, scale: 0.9 }}
                transition={{ duration: 0.3 }}
              >
                <ResultScreen
                  score={quizState.score}
                  totalQuestions={quizQuestions.length}
                  onRestart={handleStart}
                />
              </motion.div>
            )}
          </AnimatePresence>
        </main>

        {/* Footer */}
        <motion.footer
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 1 }}
          className="fixed bottom-4 left-0 right-0 text-center"
        >
          <p className="text-slate-600 text-sm">
            Drag & Drop Sort Quiz - Digital Pop Style
          </p>
        </motion.footer>
      </div>
    </div>
  );
}

export default App;
