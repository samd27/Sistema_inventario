import { motion, useReducedMotion } from 'framer-motion';
import './Card.css';
import { motionTokens } from '../utils/motionTokens';

const Card = ({ children, className = '', animate = true, delay = 0 }) => {
  const shouldReduce = useReducedMotion();

  const cardVariants = {
    hidden: { opacity: 0, y: 12 },
    visible: { 
      opacity: 1, 
      y: 0,
      transition: shouldReduce ? { duration: 0 } : { duration: motionTokens.durationBase, ease: motionTokens.ease, delay }
    }
  };
  
  if (animate) {
    return (
      <motion.div
        className={`card ${className}`}
        variants={cardVariants}
        initial="hidden"
        animate="visible"
        whileHover={shouldReduce ? {} : { y: -6, boxShadow: '0 14px 40px rgba(2,6,23,0.42)' }}
      >
        {children}
      </motion.div>
    );
  }
  
  return (
    <div className={`card ${className}`}>
      {children}
    </div>
  );
};

export default Card;
