import { motion } from 'framer-motion';
import { Button } from '@/components/ui/button';
import { Play, Sparkles, Zap, Target } from 'lucide-react';

interface StartScreenProps {
  onStart: () => void;
}

export function StartScreen({ onStart }: StartScreenProps) {
  return (
    <div className="w-full max-w-lg mx-auto">
      <motion.div
        initial={{ opacity: 0, y: 30 }}
        animate={{ opacity: 1, y: 0 }}
        className="bg-gradient-to-br from-slate-800/90 to-slate-900/90 
                   backdrop-blur-xl rounded-3xl p-8
                   border border-slate-700/50
                   shadow-[0_8px_32px_rgba(0,0,0,0.3)]
                   text-center"
      >
        {/* Logo/Title */}
        <motion.div
          initial={{ scale: 0.8, opacity: 0 }}
          animate={{ scale: 1, opacity: 1 }}
          transition={{ delay: 0.2, type: 'spring' }}
          className="mb-6"
        >
          <div className="inline-flex items-center justify-center w-24 h-24 rounded-2xl
                          bg-gradient-to-br from-cyan-400 via-fuchsia-400 to-yellow-400
                          shadow-[0_0_40px_rgba(192,38,211,0.5)]
                          mb-4"
          >
            <Zap className="w-12 h-12 text-white" />
          </div>
          
          <h1 className="text-4xl font-black text-white mb-2 tracking-tight">
            <span className="bg-gradient-to-r from-cyan-400 via-fuchsia-400 to-yellow-400 
                             bg-clip-text text-transparent"
            >
              DDソートクイズ
            </span>
          </h1>
          <p className="text-slate-400 text-lg">デジタルポップ</p>
        </motion.div>

        {/* Description */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.4 }}
          className="mb-8 space-y-4"
        >
          <p className="text-white text-lg leading-relaxed">
            4つの選択肢を<span className="text-cyan-400 font-bold">ドラッグ&ドロップ</span>で
            <br />
            正しい順序に並べ替えよう！
          </p>
          
          <div className="flex justify-center gap-4 flex-wrap">
            <div className="flex items-center gap-2 px-4 py-2 rounded-full
                            bg-cyan-500/20 border border-cyan-400/30"
            >
              <Target className="w-4 h-4 text-cyan-400" />
              <span className="text-cyan-300 text-sm font-medium">8問</span>
            </div>
            <div className="flex items-center gap-2 px-4 py-2 rounded-full
                            bg-fuchsia-500/20 border border-fuchsia-400/30"
            >
              <Sparkles className="w-4 h-4 text-fuchsia-400" />
              <span className="text-fuchsia-300 text-sm font-medium">スコア制</span>
            </div>
          </div>
        </motion.div>

        {/* Features */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.6 }}
          className="mb-8 grid grid-cols-2 gap-3"
        >
          {[
            { icon: '🖱️', text: 'ドラッグ&ドロップ' },
            { icon: '🎨', text: 'デジタルポップ' },
            { icon: '⚡', text: 'サクサク動作' },
            { icon: '🏆', text: 'ランキング表示' },
          ].map((feature, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.7 + index * 0.1 }}
              className="flex items-center gap-2 px-3 py-2 rounded-lg
                         bg-slate-700/50 border border-slate-600/50"
            >
              <span className="text-xl">{feature.icon}</span>
              <span className="text-slate-300 text-sm">{feature.text}</span>
            </motion.div>
          ))}
        </motion.div>

        {/* Start Button */}
        <motion.div
          initial={{ scale: 0.9, opacity: 0 }}
          animate={{ scale: 1, opacity: 1 }}
          transition={{ delay: 0.8 }}
        >
          <Button
            onClick={onStart}
            className="w-full bg-gradient-to-r from-cyan-500 via-fuchsia-500 to-yellow-500
                       hover:from-cyan-400 hover:via-fuchsia-400 hover:to-yellow-400
                       text-white font-bold text-xl px-10 py-7 rounded-xl
                       shadow-[0_0_30px_rgba(192,38,211,0.4)]
                       hover:shadow-[0_0_50px_rgba(192,38,211,0.6)]
                       transition-all duration-300"
          >
            <Play className="w-6 h-6 mr-2 fill-current" />
            スタート
            <Sparkles className="w-6 h-6 ml-2" />
          </Button>
        </motion.div>
      </motion.div>
    </div>
  );
}
