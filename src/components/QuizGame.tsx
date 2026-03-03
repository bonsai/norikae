import { useState, useCallback } from 'react';
import {
  DndContext,
  closestCenter,
  KeyboardSensor,
  PointerSensor,
  useSensor,
  useSensors,
  type DragEndEvent,
} from '@dnd-kit/core';
import {
  arrayMove,
  SortableContext,
  sortableKeyboardCoordinates,
  verticalListSortingStrategy,
} from '@dnd-kit/sortable';
import { motion, AnimatePresence } from 'framer-motion';
import type { QuizItem } from '@/types/quiz';
import { SortableItem } from './SortableItem';
import { Button } from '@/components/ui/button';
import { Sparkles, RotateCcw, ChevronRight, Trophy, Lightbulb } from 'lucide-react';

interface QuizGameProps {
  question: string;
  hint?: string;
  items: QuizItem[];
  questionNumber: number;
  totalQuestions: number;
  score: number;
  onAnswer: (isCorrect: boolean) => void;
  onNext: () => void;
}

export function QuizGame({
  question,
  hint,
  items: initialItems,
  questionNumber,
  totalQuestions,
  score,
  onAnswer,
  onNext,
}: QuizGameProps) {
  const [items, setItems] = useState<QuizItem[]>(
    [...initialItems].sort(() => Math.random() - 0.5)
  );
  const [isAnswered, setIsAnswered] = useState(false);
  const [isCorrect, setIsCorrect] = useState(false);
  const [showHint, setShowHint] = useState(false);

  const sensors = useSensors(
    useSensor(PointerSensor, {
      activationConstraint: {
        distance: 8,
      },
    }),
    useSensor(KeyboardSensor, {
      coordinateGetter: sortableKeyboardCoordinates,
    })
  );

  const handleDragEnd = useCallback((event: DragEndEvent) => {
    const { active, over } = event;

    if (over && active.id !== over.id) {
      setItems((items) => {
        const oldIndex = items.findIndex((item) => item.id === active.id);
        const newIndex = items.findIndex((item) => item.id === over.id);
        return arrayMove(items, oldIndex, newIndex);
      });
    }
  }, []);

  const checkAnswer = () => {
    const currentOrder = items.map((item, index) => ({
      ...item,
      currentPosition: index + 1,
    }));

    const allCorrect = currentOrder.every(
      (item) => item.currentPosition === item.order
    );

    setIsCorrect(allCorrect);
    setIsAnswered(true);
    onAnswer(allCorrect);
  };

  const handleNext = () => {
    setItems([...initialItems].sort(() => Math.random() - 0.5));
    setIsAnswered(false);
    setIsCorrect(false);
    setShowHint(false);
    onNext();
  };

  const progress = (questionNumber / totalQuestions) * 100;

  return (
    <div className="w-full max-w-2xl mx-auto">
      {/* Progress Bar */}
      <div className="mb-6">
        <div className="flex justify-between items-center mb-2">
          <span className="text-cyan-300 text-sm font-medium">
            問題 {questionNumber} / {totalQuestions}
          </span>
          <span className="text-fuchsia-300 text-sm font-medium flex items-center gap-1">
            <Trophy className="w-4 h-4" />
            スコア: {score}
          </span>
        </div>
        <div className="h-3 bg-slate-800 rounded-full overflow-hidden border border-slate-700">
          <motion.div
            className="h-full bg-gradient-to-r from-cyan-400 via-fuchsia-400 to-yellow-400"
            initial={{ width: 0 }}
            animate={{ width: `${progress}%` }}
            transition={{ duration: 0.5, ease: 'easeOut' }}
          />
        </div>
      </div>

      {/* Question Card */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="bg-gradient-to-br from-slate-800/90 to-slate-900/90 
                   backdrop-blur-xl rounded-2xl p-6 mb-6
                   border border-slate-700/50
                   shadow-[0_8px_32px_rgba(0,0,0,0.3)]"
      >
        <h2 className="text-2xl font-bold text-white mb-4 leading-relaxed">
          {question}
        </h2>

        {/* Hint Section */}
        {hint && !isAnswered && (
          <div className="mb-4">
            <button
              onClick={() => setShowHint(!showHint)}
              className="flex items-center gap-2 text-amber-400 hover:text-amber-300 
                         transition-colors text-sm font-medium"
            >
              <Lightbulb className="w-4 h-4" />
              {showHint ? 'ヒントを隠す' : 'ヒントを見る'}
            </button>
            <AnimatePresence>
              {showHint && (
                <motion.div
                  initial={{ opacity: 0, height: 0 }}
                  animate={{ opacity: 1, height: 'auto' }}
                  exit={{ opacity: 0, height: 0 }}
                  className="mt-2 p-3 bg-amber-500/10 border border-amber-400/30 
                             rounded-lg text-amber-200 text-sm"
                >
                  💡 {hint}
                </motion.div>
              )}
            </AnimatePresence>
          </div>
        )}

        {/* Sortable List */}
        <DndContext
          sensors={sensors}
          collisionDetection={closestCenter}
          onDragEnd={handleDragEnd}
        >
          <SortableContext
            items={items.map((item) => item.id)}
            strategy={verticalListSortingStrategy}
          >
            <div className="space-y-3">
              {items.map((item, index) => (
                <SortableItem
                  key={item.id}
                  id={item.id}
                  text={item.text}
                  index={index}
                  isAnswered={isAnswered}
                  correctOrder={item.order}
                />
              ))}
            </div>
          </SortableContext>
        </DndContext>

        {/* Result Message */}
        <AnimatePresence>
          {isAnswered && (
            <motion.div
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0, scale: 0.9 }}
              className={`mt-6 p-4 rounded-xl text-center font-bold text-lg
                         ${isCorrect 
                           ? 'bg-gradient-to-r from-green-500/20 to-emerald-500/20 border-2 border-green-400 text-green-300' 
                           : 'bg-gradient-to-r from-rose-500/20 to-pink-500/20 border-2 border-rose-400 text-rose-300'
                         }`}
            >
              {isCorrect ? (
                <span className="flex items-center justify-center gap-2">
                  <Sparkles className="w-6 h-6" />
                  正解！すごい！
                  <Sparkles className="w-6 h-6" />
                </span>
              ) : (
                <span className="flex items-center justify-center gap-2">
                  <RotateCcw className="w-6 h-6" />
                  残念... もう一度挑戦してみよう！
                </span>
              )}
            </motion.div>
          )}
        </AnimatePresence>
      </motion.div>

      {/* Action Buttons */}
      <div className="flex justify-center gap-4">
        {!isAnswered ? (
          <Button
            onClick={checkAnswer}
            className="bg-gradient-to-r from-cyan-500 to-blue-500 
                       hover:from-cyan-400 hover:to-blue-400
                       text-white font-bold text-lg px-8 py-6 rounded-xl
                       shadow-[0_0_20px_rgba(6,182,212,0.4)]
                       hover:shadow-[0_0_30px_rgba(6,182,212,0.6)]
                       transition-all duration-300"
          >
            <Sparkles className="w-5 h-5 mr-2" />
            答え合わせ
          </Button>
        ) : (
          <Button
            onClick={handleNext}
            className="bg-gradient-to-r from-fuchsia-500 to-purple-500 
                       hover:from-fuchsia-400 hover:to-purple-400
                       text-white font-bold text-lg px-8 py-6 rounded-xl
                       shadow-[0_0_20px_rgba(192,38,211,0.4)]
                       hover:shadow-[0_0_30px_rgba(192,38,211,0.6)]
                       transition-all duration-300"
          >
            次の問題へ
            <ChevronRight className="w-5 h-5 ml-2" />
          </Button>
        )}
      </div>
    </div>
  );
}
