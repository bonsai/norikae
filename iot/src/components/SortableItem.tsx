import { useSortable } from '@dnd-kit/sortable';
import { CSS } from '@dnd-kit/utilities';
import { motion } from 'framer-motion';

interface SortableItemProps {
  id: string;
  text: string;
  index: number;
  isAnswered: boolean;
  correctOrder: number;
}

export function SortableItem({ 
  id, 
  text, 
  index, 
  isAnswered,
  correctOrder 
}: SortableItemProps) {
  const {
    attributes,
    listeners,
    setNodeRef,
    transform,
    transition,
    isDragging,
  } = useSortable({ id });

  const style = {
    transform: CSS.Transform.toString(transform),
    transition,
  };

  const getBorderColor = () => {
    if (!isAnswered) return 'border-cyan-400/50';
    const currentOrder = index + 1;
    if (currentOrder === correctOrder) return 'border-green-400';
    return 'border-rose-400';
  };

  const getBgColor = () => {
    if (!isAnswered) return 'bg-slate-800/80';
    const currentOrder = index + 1;
    if (currentOrder === correctOrder) return 'bg-green-500/20';
    return 'bg-rose-500/20';
  };

  const getGlowEffect = () => {
    if (!isAnswered) return 'hover:shadow-[0_0_20px_rgba(34,211,238,0.4)]';
    const currentOrder = index + 1;
    if (currentOrder === correctOrder) return 'shadow-[0_0_20px_rgba(74,222,128,0.5)]';
    return 'shadow-[0_0_20px_rgba(251,113,133,0.5)]';
  };

  return (
    <motion.div
      ref={setNodeRef}
      style={style}
      {...attributes}
      {...listeners}
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: index * 0.1 }}
      className={`
        relative cursor-grab active:cursor-grabbing
        px-6 py-4 rounded-xl
        border-2 ${getBorderColor()}
        ${getBgColor()}
        backdrop-blur-md
        transition-all duration-300
        ${getGlowEffect()}
        ${isDragging ? 'scale-105 z-50 shadow-2xl' : 'scale-100'}
        select-none
      `}
    >
      {/* Order Number Badge */}
      <div className={`
        absolute -left-3 -top-3 w-8 h-8 rounded-full
        flex items-center justify-center
        text-sm font-bold
        ${!isAnswered 
          ? 'bg-gradient-to-br from-cyan-400 to-blue-500 text-white' 
          : index + 1 === correctOrder
            ? 'bg-gradient-to-br from-green-400 to-emerald-500 text-white'
            : 'bg-gradient-to-br from-rose-400 to-pink-500 text-white'
        }
        shadow-lg
      `}>
        {index + 1}
      </div>

      {/* Drag Handle Icon */}
      <div className="absolute right-3 top-1/2 -translate-y-1/2 opacity-50">
        <svg 
          width="20" 
          height="20" 
          viewBox="0 0 20 20" 
          fill="none"
          className="text-white/60"
        >
          <path 
            d="M7 5h2v2H7V5zm0 4h2v2H7V9zm0 4h2v2H7v-2zm6-8h2v2h-2V5zm0 4h2v2h-2V9zm0 4h2v2h-2v-2z" 
            fill="currentColor"
          />
        </svg>
      </div>

      {/* Content */}
      <span className="text-white font-medium text-lg pr-8 block">
        {text}
      </span>

      {/* Correct Order Indicator (shown after answer) */}
      {isAnswered && index + 1 !== correctOrder && (
        <motion.div
          initial={{ opacity: 0, scale: 0 }}
          animate={{ opacity: 1, scale: 1 }}
          className="absolute -right-2 -bottom-2 bg-green-500 text-white text-xs font-bold px-2 py-1 rounded-full shadow-lg"
        >
          正解: {correctOrder}番目
        </motion.div>
      )}
    </motion.div>
  );
}
