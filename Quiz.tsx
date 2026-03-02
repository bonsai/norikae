/**
 * NORIKAE MASTER - 東京メトロ乗り換え4択クイズ
 *
 * Design Philosophy: "でんしゃいろ" (Densha-iro)
 * - 路線カラーを大胆に使ったグラデーション背景
 * - 丸みたっぷりのカード（子ども向け）
 * - アニメーションで正解・不正解を楽しく演出
 * - フォント: Rounded / 大きめ / 読みやすい
 * - モバイルファースト（縦スクロールなし1画面完結）
 */

import { useState, useEffect, useCallback } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { QUIZ_QUESTIONS, DIFFICULTY_LABELS, LINE_COLORS, type QuizQuestion } from '@/data/quizData';

// ─── 型定義 ───────────────────────────────────────────────
type GameState = 'title' | 'select' | 'playing' | 'result';
type AnswerState = 'idle' | 'correct' | 'wrong';

// ─── ユーティリティ ────────────────────────────────────────
function shuffle<T>(arr: T[]): T[] {
  const a = [...arr];
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [a[i], a[j]] = [a[j], a[i]];
  }
  return a;
}

function hexToRgb(hex: string) {
  const r = parseInt(hex.slice(1, 3), 16);
  const g = parseInt(hex.slice(3, 5), 16);
  const b = parseInt(hex.slice(5, 7), 16);
  return `${r}, ${g}, ${b}`;
}

// ─── 定数 ──────────────────────────────────────────────────
const CHOICE_COLORS = ['#E53E3E', '#3182CE', '#38A169', '#D69E2E'];
const CHOICE_LABELS = ['A', 'B', 'C', 'D'];

// ─── サブコンポーネント ────────────────────────────────────

/** 路線カラーバッジ */
function LineBadge({ name, color }: { name: string; color: string }) {
  return (
    <span
      className="inline-flex items-center px-2 py-0.5 rounded-full text-white text-xs font-bold"
      style={{ backgroundColor: color, fontSize: '11px' }}
    >
      {name}
    </span>
  );
}

/** 星アイコン */
function Stars({ count }: { count: number }) {
  return (
    <span className="text-yellow-400 text-sm">
      {'★'.repeat(count)}{'☆'.repeat(3 - count)}
    </span>
  );
}

/** タイトル画面 */
function TitleScreen({ onStart }: { onStart: () => void }) {
  return (
    <motion.div
      className="flex flex-col items-center justify-center h-full px-6 text-center"
      initial={{ opacity: 0, scale: 0.9 }}
      animate={{ opacity: 1, scale: 1 }}
      exit={{ opacity: 0, scale: 1.1 }}
      transition={{ duration: 0.4 }}
    >
      {/* 路線カラーの円たち - 直接カラー指定 */}
      <div className="relative mb-6">
        <div className="flex gap-2 justify-center mb-2">
          {['#F5A623','#E60012','#9B9EA0','#009BBF','#00BB85'].map((c, i) => (
            <motion.div
              key={i}
              className="w-9 h-9 rounded-full shadow-md"
              style={{ backgroundColor: c }}
              animate={{ y: [0, -8, 0] }}
              transition={{ duration: 1.2, delay: i * 0.15, repeat: Infinity }}
            />
          ))}
        </div>
        <div className="flex gap-2 justify-center">
          {['#C1A900','#8F76D6','#00AC9B','#9C5E31'].map((c, i) => (
            <motion.div
              key={i}
              className="w-9 h-9 rounded-full shadow-md"
              style={{ backgroundColor: c }}
              animate={{ y: [0, -8, 0] }}
              transition={{ duration: 1.2, delay: (i + 5) * 0.15, repeat: Infinity }}
            />
          ))}
        </div>
      </div>

      <motion.div
        animate={{ rotate: [-2, 2, -2] }}
        transition={{ duration: 2, repeat: Infinity }}
        className="text-5xl mb-3"
      >
        🚇
      </motion.div>

      <h1 className="text-5xl font-black tracking-tight mb-1" style={{ color: '#0d0d2b', fontFamily: "'Rounded Mplus 1c', 'M PLUS Rounded 1c', sans-serif", textShadow: '0 2px 8px rgba(0,0,0,0.08)' }}>
        NORIKAE
      </h1>
      <h1 className="text-5xl font-black tracking-tight mb-2" style={{ color: '#0d0d2b', fontFamily: "'Rounded Mplus 1c', 'M PLUS Rounded 1c', sans-serif", textShadow: '0 2px 8px rgba(0,0,0,0.08)' }}>
        MASTER
      </h1>
      <p className="text-base font-bold mb-1" style={{ color: '#444' }}>東京メトロ のりかえクイズ</p>
      <p className="text-sm font-bold mb-8" style={{ color: '#888' }}>全{QUIZ_QUESTIONS.length}問</p>

      <motion.button
        onClick={onStart}
        className="w-full max-w-xs py-5 rounded-3xl text-white text-xl font-black shadow-xl"
        style={{ background: 'linear-gradient(135deg, #E60012 0%, #F5A623 100%)', boxShadow: '0 8px 24px rgba(230,0,18,0.35)' }}
        whileHover={{ scale: 1.05 }}
        whileTap={{ scale: 0.95 }}
      >
        🎮 はじめる！
      </motion.button>

      <p className="text-xs text-gray-400 mt-4">タップしてスタート</p>
    </motion.div>
  );
}

/** 難易度選択画面 */
function SelectScreen({ onSelect }: { onSelect: (mode: 'all' | 'easy' | 'normal' | 'hard') => void }) {
  const modes: { key: 'easy' | 'normal' | 'hard' | 'all'; label: string; desc: string; color: string; emoji: string }[] = [
    { key: 'easy',   label: 'かんたん',     desc: '⭐ 6もん',    color: '#4CAF50', emoji: '😊' },
    { key: 'normal', label: 'ふつう',       desc: '⭐⭐ 6もん',  color: '#FF9800', emoji: '😤' },
    { key: 'hard',   label: 'むずかしい',   desc: '⭐⭐⭐ 6もん', color: '#F44336', emoji: '🔥' },
    { key: 'all',    label: 'ぜんぶ',       desc: '全18もん',    color: '#9C27B0', emoji: '🏆' },
  ];

  return (
    <motion.div
      className="flex flex-col h-full px-5 py-6"
      initial={{ opacity: 0, x: 40 }}
      animate={{ opacity: 1, x: 0 }}
      exit={{ opacity: 0, x: -40 }}
    >
      <div className="text-center mb-6">
        <div className="text-3xl mb-2">🎯</div>
        <h2 className="text-2xl font-black text-gray-800">レベルをえらぼう！</h2>
        <p className="text-sm text-gray-500 mt-1">すきなレベルをタップしてね</p>
      </div>

      <div className="flex flex-col gap-4 flex-1 justify-center">
        {modes.map((m, i) => (
          <motion.button
            key={m.key}
            onClick={() => onSelect(m.key)}
            className="flex items-center gap-4 p-5 rounded-3xl text-white shadow-md"
            style={{ background: `linear-gradient(135deg, ${m.color}dd, ${m.color}99)` }}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: i * 0.1 }}
            whileHover={{ scale: 1.03, x: 4 }}
            whileTap={{ scale: 0.97 }}
          >
            <span className="text-4xl">{m.emoji}</span>
            <div className="text-left flex-1">
              <div className="text-xl font-black">{m.label}</div>
              <div className="text-sm opacity-80">{m.desc}</div>
            </div>
            <span className="text-2xl">→</span>
          </motion.button>
        ))}
      </div>
    </motion.div>
  );
}

/** 選択肢ボタン */
function ChoiceButton({
  label, text, color, state, onClick, disabled
}: {
  label: string;
  text: string;
  color: string;
  state: 'idle' | 'correct' | 'wrong' | 'dim';
  onClick: () => void;
  disabled: boolean;
}) {
  const bgMap = {
    idle:    `${color}22`,
    correct: color,
    wrong:   '#ef444422',
    dim:     '#f3f4f6',
  };
  const borderMap = {
    idle:    `2px solid ${color}66`,
    correct: `2px solid ${color}`,
    wrong:   '2px solid #ef444466',
    dim:     '2px solid #e5e7eb',
  };
  const textMap = {
    idle:    '#1a1a2e',
    correct: '#ffffff',
    wrong:   '#9ca3af',
    dim:     '#9ca3af',
  };

  return (
    <motion.button
      onClick={onClick}
      disabled={disabled}
      className="flex items-center gap-3 w-full p-4 rounded-2xl text-left"
      style={{
        background: bgMap[state],
        border: borderMap[state],
        color: textMap[state],
      }}
      whileHover={!disabled ? { scale: 1.02 } : {}}
      whileTap={!disabled ? { scale: 0.98 } : {}}
      animate={state === 'correct' ? { scale: [1, 1.04, 1] } : {}}
      transition={{ duration: 0.3 }}
    >
      <span
        className="flex-shrink-0 w-9 h-9 rounded-full flex items-center justify-center font-black text-base"
        style={{
          background: state === 'correct' ? 'rgba(255,255,255,0.3)' : `${color}33`,
          color: state === 'correct' ? '#fff' : color,
        }}
      >
        {state === 'correct' ? '✓' : state === 'wrong' ? '✗' : label}
      </span>
      <span className="font-bold text-sm leading-snug">{text}</span>
    </motion.button>
  );
}

/** クイズプレイ画面 */
function PlayScreen({
  questions,
  onFinish,
}: {
  questions: QuizQuestion[];
  onFinish: (score: number, total: number) => void;
}) {
  const [idx, setIdx] = useState(0);
  const [score, setScore] = useState(0);
  const [answerState, setAnswerState] = useState<AnswerState>('idle');
  const [selectedIdx, setSelectedIdx] = useState<number | null>(null);
  const [showExplanation, setShowExplanation] = useState(false);

  const q = questions[idx];
  const progress = ((idx) / questions.length) * 100;

  const handleAnswer = useCallback((choiceIdx: number) => {
    if (answerState !== 'idle') return;
    setSelectedIdx(choiceIdx);
    if (choiceIdx === q.correctIndex) {
      setAnswerState('correct');
      setScore(s => s + 1);
    } else {
      setAnswerState('wrong');
    }
    setShowExplanation(true);
  }, [answerState, q.correctIndex]);

  const handleNext = useCallback(() => {
    if (idx + 1 >= questions.length) {
      onFinish(score + (answerState === 'correct' ? 0 : 0), questions.length);
      // scoreはuseCallbackの外で計算
    } else {
      setIdx(i => i + 1);
      setAnswerState('idle');
      setSelectedIdx(null);
      setShowExplanation(false);
    }
  }, [idx, questions.length, onFinish, score, answerState]);

  // 正解スコアを正確に渡すため
  const handleNextWithScore = useCallback(() => {
    const finalScore = answerState === 'correct' ? score : score;
    if (idx + 1 >= questions.length) {
      onFinish(finalScore, questions.length);
    } else {
      setIdx(i => i + 1);
      setAnswerState('idle');
      setSelectedIdx(null);
      setShowExplanation(false);
    }
  }, [idx, questions.length, onFinish, score, answerState]);

  const diffInfo = DIFFICULTY_LABELS[q.difficulty];

  // グラデーション背景色
  const c1 = q.lineColor;
  const c2 = q.lineColor2 || q.lineColor;

  return (
    <motion.div
      key={idx}
      className="flex flex-col h-full"
      initial={{ opacity: 0, x: 30 }}
      animate={{ opacity: 1, x: 0 }}
      exit={{ opacity: 0, x: -30 }}
      transition={{ duration: 0.3 }}
    >
      {/* ヘッダー：進捗 */}
      <div
        className="px-5 pt-5 pb-4 rounded-b-3xl"
        style={{ background: `linear-gradient(135deg, ${c1}, ${c2})` }}
      >
        <div className="flex items-center justify-between mb-3">
          <div className="flex gap-1 items-center">
            <LineBadge name={q.lineName} color="rgba(255,255,255,0.3)" />
            {q.lineName2 && <LineBadge name={q.lineName2} color="rgba(255,255,255,0.3)" />}
          </div>
          <span className="text-white font-black text-sm opacity-90">
            {idx + 1} / {questions.length}
          </span>
        </div>

        {/* プログレスバー */}
        <div className="w-full h-2 rounded-full bg-white/30 overflow-hidden">
          <motion.div
            className="h-full rounded-full bg-white"
            initial={{ width: `${progress}%` }}
            animate={{ width: `${((idx + 1) / questions.length) * 100}%` }}
            transition={{ duration: 0.4 }}
          />
        </div>

        <div className="flex items-center justify-between mt-2">
          <div className="flex items-center gap-1">
            <Stars count={q.difficulty === 'easy' ? 1 : q.difficulty === 'normal' ? 2 : 3} />
            <span className="text-white/80 text-xs">{diffInfo.label}</span>
          </div>
          <span className="text-white font-black text-sm">
            スコア: {score}
          </span>
        </div>
      </div>

      {/* 問題文 */}
      <div className="px-5 py-4 flex-shrink-0">
        <div className="flex items-start gap-3">
          <span className="text-3xl flex-shrink-0">{q.emoji}</span>
          <p
            className="font-black text-gray-800 leading-snug"
            style={{ fontSize: '17px', whiteSpace: 'pre-line' }}
          >
            {q.question}
          </p>
        </div>
        {q.hint && answerState === 'idle' && (
          <motion.div
            className="mt-2 px-3 py-1.5 rounded-xl text-xs font-bold text-gray-500"
            style={{ background: '#f3f4f6' }}
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 1.5 }}
          >
            💡 ヒント: {q.hint}
          </motion.div>
        )}
      </div>

      {/* 選択肢 */}
      <div className="px-5 flex flex-col gap-2.5 flex-1">
        {q.choices.map((choice, i) => {
          let state: 'idle' | 'correct' | 'wrong' | 'dim' = 'idle';
          if (answerState !== 'idle') {
            if (i === q.correctIndex) state = 'correct';
            else if (i === selectedIdx) state = 'wrong';
            else state = 'dim';
          }
          return (
            <ChoiceButton
              key={i}
              label={CHOICE_LABELS[i]}
              text={choice}
              color={CHOICE_COLORS[i]}
              state={state}
              onClick={() => handleAnswer(i)}
              disabled={answerState !== 'idle'}
            />
          );
        })}
      </div>

      {/* 解説・次へボタン */}
      <AnimatePresence>
        {showExplanation && (
          <motion.div
            className="px-5 pb-5 pt-3"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: 20 }}
          >
            {/* 正解・不正解バナー */}
            <div
              className="rounded-2xl p-3 mb-3 text-center"
              style={{
                background: answerState === 'correct'
                  ? 'linear-gradient(135deg, #4CAF50, #8BC34A)'
                  : 'linear-gradient(135deg, #F44336, #FF5722)',
              }}
            >
              <p className="text-white font-black text-lg">
                {answerState === 'correct' ? '🎉 せいかい！' : '😢 ざんねん…'}
              </p>
            </div>

            {/* 解説 */}
            <div
              className="rounded-2xl p-3 mb-3 text-sm text-gray-700 leading-relaxed font-medium"
              style={{ background: '#f8f9fa', border: '2px solid #e9ecef' }}
            >
              {q.explanation}
            </div>

            {/* 次へボタン */}
            <motion.button
              onClick={handleNextWithScore}
              className="w-full py-4 rounded-3xl text-white font-black text-lg shadow-md"
              style={{ background: `linear-gradient(135deg, ${c1}, ${c2})` }}
              whileHover={{ scale: 1.03 }}
              whileTap={{ scale: 0.97 }}
            >
              {idx + 1 >= questions.length ? '🏁 けっかをみる！' : '→ つぎのもんだい'}
            </motion.button>
          </motion.div>
        )}
      </AnimatePresence>
    </motion.div>
  );
}

/** 結果画面 */
function ResultScreen({
  score,
  total,
  onRetry,
  onHome,
}: {
  score: number;
  total: number;
  onRetry: () => void;
  onHome: () => void;
}) {
  const pct = Math.round((score / total) * 100);
  const rank =
    pct === 100 ? { label: 'のりかえマスター！', emoji: '👑', color: '#F5A623' } :
    pct >= 80  ? { label: 'のりかえはかせ！',   emoji: '🎓', color: '#9C27B0' } :
    pct >= 60  ? { label: 'のりかえじょうず！', emoji: '⭐', color: '#2196F3' } :
    pct >= 40  ? { label: 'もう少し！',         emoji: '💪', color: '#4CAF50' } :
                 { label: 'れんしゅうしよう！', emoji: '📚', color: '#FF9800' };

  // 路線カラーを使ったグラデーション
  const allColors = Object.values(LINE_COLORS);

  return (
    <motion.div
      className="flex flex-col items-center justify-center h-full px-6 text-center"
      initial={{ opacity: 0, scale: 0.8 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ type: 'spring', stiffness: 200, damping: 20 }}
    >
      {/* 路線カラーの虹 */}
      <div className="flex gap-1.5 mb-5">
        {allColors.map((c, i) => (
          <motion.div
            key={i}
            className="w-5 h-5 rounded-full"
            style={{ backgroundColor: c }}
            initial={{ scale: 0 }}
            animate={{ scale: 1 }}
            transition={{ delay: i * 0.08, type: 'spring' }}
          />
        ))}
      </div>

      <motion.div
        className="text-7xl mb-4"
        animate={{ rotate: [0, -10, 10, -10, 0] }}
        transition={{ duration: 0.6, delay: 0.5 }}
      >
        {rank.emoji}
      </motion.div>

      <h2
        className="text-2xl font-black mb-1"
        style={{ color: rank.color }}
      >
        {rank.label}
      </h2>

      {/* スコア円グラフ風 */}
      <div
        className="w-36 h-36 rounded-full flex flex-col items-center justify-center my-5 shadow-lg"
        style={{ background: `conic-gradient(${rank.color} ${pct * 3.6}deg, #e5e7eb ${pct * 3.6}deg)` }}
      >
        <div className="w-28 h-28 rounded-full bg-white flex flex-col items-center justify-center">
          <span className="text-4xl font-black" style={{ color: rank.color }}>{score}</span>
          <span className="text-sm text-gray-500 font-bold">/ {total}もん</span>
        </div>
      </div>

      <p className="text-gray-500 font-bold mb-8">
        せいかいりつ <span className="text-2xl font-black" style={{ color: rank.color }}>{pct}%</span>
      </p>

      <div className="flex flex-col gap-3 w-full max-w-xs">
        <motion.button
          onClick={onRetry}
          className="w-full py-4 rounded-3xl text-white font-black text-lg shadow-md"
          style={{ background: `linear-gradient(135deg, ${rank.color}, ${rank.color}aa)` }}
          whileHover={{ scale: 1.04 }}
          whileTap={{ scale: 0.96 }}
        >
          🔄 もういちど！
        </motion.button>
        <motion.button
          onClick={onHome}
          className="w-full py-4 rounded-3xl font-black text-lg"
          style={{ background: '#f3f4f6', color: '#374151', border: '2px solid #e5e7eb' }}
          whileHover={{ scale: 1.04 }}
          whileTap={{ scale: 0.96 }}
        >
          🏠 トップへ
        </motion.button>
      </div>
    </motion.div>
  );
}

// ─── メインコンポーネント ──────────────────────────────────
export default function Quiz() {
  const [gameState, setGameState] = useState<GameState>('title');
  const [questions, setQuestions] = useState<QuizQuestion[]>([]);
  const [finalScore, setFinalScore] = useState(0);
  const [finalTotal, setFinalTotal] = useState(0);
  const [selectedMode, setSelectedMode] = useState<'all' | 'easy' | 'normal' | 'hard'>('all');

  const handleSelectMode = (mode: 'all' | 'easy' | 'normal' | 'hard') => {
    setSelectedMode(mode);
    const filtered = mode === 'all'
      ? QUIZ_QUESTIONS
      : QUIZ_QUESTIONS.filter(q => q.difficulty === mode);
    setQuestions(shuffle(filtered));
    setGameState('playing');
  };

  const handleFinish = (score: number, total: number) => {
    setFinalScore(score);
    setFinalTotal(total);
    setGameState('result');
  };

  const handleRetry = () => {
    const filtered = selectedMode === 'all'
      ? QUIZ_QUESTIONS
      : QUIZ_QUESTIONS.filter(q => q.difficulty === selectedMode);
    setQuestions(shuffle(filtered));
    setGameState('playing');
  };

  return (
    <div
      className="min-h-screen flex items-center justify-center"
      style={{ background: 'linear-gradient(160deg, #e8f0ff 0%, #ffe8e8 50%, #e8fff0 100%)' }}
    >
      {/* モバイルフレーム */}
      <div
        className="relative w-full overflow-hidden bg-white shadow-2xl"
        style={{
          maxWidth: '390px',
          minHeight: '100svh',
          maxHeight: '100svh',
          borderRadius: window.innerWidth > 430 ? '40px' : '0',
          display: 'flex',
          flexDirection: 'column',
        }}
      >
        {/* 上部装飾バー（路線カラー） */}
        <div className="flex h-1.5 flex-shrink-0">
          {Object.values(LINE_COLORS).map((c, i) => (
            <div key={i} className="flex-1" style={{ backgroundColor: c }} />
          ))}
        </div>

        {/* コンテンツ */}
        <div className="flex-1 overflow-hidden relative">
          <AnimatePresence mode="wait">
            {gameState === 'title' && (
              <motion.div key="title" className="absolute inset-0">
                <TitleScreen onStart={() => setGameState('select')} />
              </motion.div>
            )}
            {gameState === 'select' && (
              <motion.div key="select" className="absolute inset-0">
                <SelectScreen onSelect={handleSelectMode} />
              </motion.div>
            )}
            {gameState === 'playing' && (
              <motion.div key="playing" className="absolute inset-0 overflow-y-auto">
                <PlayScreen questions={questions} onFinish={handleFinish} />
              </motion.div>
            )}
            {gameState === 'result' && (
              <motion.div key="result" className="absolute inset-0 overflow-y-auto">
                <ResultScreen
                  score={finalScore}
                  total={finalTotal}
                  onRetry={handleRetry}
                  onHome={() => setGameState('title')}
                />
              </motion.div>
            )}
          </AnimatePresence>
        </div>

        {/* 下部装飾バー（路線カラー逆順） */}
        <div className="flex h-1.5 flex-shrink-0">
          {Object.values(LINE_COLORS).reverse().map((c, i) => (
            <div key={i} className="flex-1" style={{ backgroundColor: c }} />
          ))}
        </div>
      </div>
    </div>
  );
}
