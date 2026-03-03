import { motion } from 'framer-motion';
import { Button } from '@/components/ui/button';
import { Star, RotateCcw, Sparkles, Medal } from 'lucide-react';

interface ResultScreenProps {
  score: number;
  totalQuestions: number;
  onRestart: () => void;
}

export function ResultScreen({ score, totalQuestions, onRestart }: ResultScreenProps) {
  const percentage = Math.round((score / totalQuestions) * 100);
  
  const getRank = () => {
    if (percentage === 100) return { icon: '👑', label: 'パーフェクト！', color: 'from-yellow-400 to-amber-500' };
    if (percentage >= 80) return { icon: '🌟', label: 'すばらしい！', color: 'from-cyan-400 to-blue-500' };
    if (percentage >= 60) return { icon: '✨', label: 'よくできた！', color: 'from-fuchsia-400 to-purple-500' };
    if (percentage >= 40) return { icon: '💪', label: 'がんばったね！', color: 'from-green-400 to-emerald-500' };
    return { icon: '🌱', label: 'また挑戦してね！', color: 'from-rose-400 to-pink-500' };
  };

  const rank = getRank();

  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.9 }}
      animate={{ opacity: 1, scale: 1 }}
      className="w-full max-w-lg mx-auto"
    >
      <div className="bg-gradient-to-br from-slate-800/90 to-slate-900/90 
                      backdrop-blur-xl rounded-3xl p-8
                      border border-slate-700/50
                      shadow-[0_8px_32px_rgba(0,0,0,0.3)]
                      text-center"
      >
        {/* Title */}
        <motion.div
          initial={{ y: -20, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ delay: 0.2 }}
        >
          <h2 className="text-3xl font-bold text-white mb-2">
            クイズ完了！
          </h2>
          <p className="text-slate-400">お疲れさまでした</p>
        </motion.div>

        {/* Score Circle */}
        <motion.div
          initial={{ scale: 0 }}
          animate={{ scale: 1 }}
          transition={{ delay: 0.4, type: 'spring' }}
          className="my-8"
        >
          <div className="relative inline-block">
            <div className="w-40 h-40 rounded-full bg-gradient-to-br from-slate-700 to-slate-800 
                            border-4 border-slate-600 flex items-center justify-center
                            shadow-[0_0_40px_rgba(0,0,0,0.3)]"
            >
              <div className="text-center">
                <div className="text-5xl font-bold text-white">
                  {score}
                </div>
                <div className="text-slate-400 text-sm">
                  / {totalQuestions} 問
                </div>
              </div>
            </div>
            
            {/* Floating Stars */}
            <motion.div
              animate={{ rotate: 360 }}
              transition={{ duration: 20, repeat: Infinity, ease: 'linear' }}
              className="absolute inset-0"
            >
              <Star className="absolute -top-2 left-1/2 -translate-x-1/2 w-6 h-6 text-yellow-400 fill-yellow-400" />
              <Star className="absolute -bottom-2 left-1/2 -translate-x-1/2 w-5 h-5 text-cyan-400 fill-cyan-400" />
              <Star className="absolute top-1/2 -left-4 -translate-y-1/2 w-4 h-4 text-fuchsia-400 fill-fuchsia-400" />
              <Star className="absolute top-1/2 -right-4 -translate-y-1/2 w-5 h-5 text-green-400 fill-green-400" />
            </motion.div>
          </div>
        </motion.div>

        {/* Percentage */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.6 }}
          className="mb-6"
        >
          <div className="text-4xl font-bold bg-gradient-to-r from-cyan-400 via-fuchsia-400 to-yellow-400 
                          bg-clip-text text-transparent"
          >
            {percentage}%
          </div>
        </motion.div>

        {/* Rank Badge */}
        <motion.div
          initial={{ y: 20, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ delay: 0.8 }}
          className="mb-8"
        >
          <div className={`inline-flex items-center gap-3 px-6 py-3 rounded-full
                          bg-gradient-to-r ${rank.color}
                          shadow-[0_0_30px_rgba(0,0,0,0.3)]`}
          >
            <Medal className="w-6 h-6 text-white" />
            <span className="text-2xl">{rank.icon}</span>
            <span className="text-white font-bold text-lg">{rank.label}</span>
            <Medal className="w-6 h-6 text-white" />
          </div>
        </motion.div>

        {/* Restart Button */}
        <motion.div
          initial={{ y: 20, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ delay: 1 }}
        >
          <Button
            onClick={onRestart}
            className="bg-gradient-to-r from-cyan-500 via-fuchsia-500 to-yellow-500
                       hover:from-cyan-400 hover:via-fuchsia-400 hover:to-yellow-400
                       text-white font-bold text-lg px-10 py-6 rounded-xl
                       shadow-[0_0_30px_rgba(192,38,211,0.4)]
                       hover:shadow-[0_0_40px_rgba(192,38,211,0.6)]
                       transition-all duration-300"
          >
            <RotateCcw className="w-5 h-5 mr-2" />
            もう一度プレイ
            <Sparkles className="w-5 h-5 ml-2" />
          </Button>
        </motion.div>
      </div>
    </motion.div>
  );
}
