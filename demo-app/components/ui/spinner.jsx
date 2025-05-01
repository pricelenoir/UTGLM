import React from 'react';
import { Loader2 } from 'lucide-react';
import { cn } from '@/lib/utils';

export function Spinner({ size = 'medium', show = true, children, className }) {
  const spinnerClasses = show
    ? 'flex flex-col items-center justify-center'
    : 'hidden';

  const sizeMap = {
    small: 'size-6',
    medium: 'size-8',
    large: 'size-12',
  };

  const loaderSize = sizeMap[size] || sizeMap.medium;

  return (
    <span className={cn(spinnerClasses)}>
      <Loader2 className={cn('animate-spin text-primary', loaderSize, className)} />
      {children}
    </span>
  );
}
