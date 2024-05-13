module Etc where

newtype Bit = Bit Bool

instance Show Bit where
  show a = [bitToChar a]
    where
      bitToChar (Bit True) = '1'
      bitToChar _ = '0'

type Matrix a = [[a]]

matDims :: Matrix a -> (Int, Int)
matDims a = (height, width)
  where
    height = length a
    width = maximum $ map length a

indexed :: [a] -> [(Int, a)]
indexed = zip [0 ..]

bitsOf :: Int -> Int -> [Bit]
bitsOf x s
  | s <= 0 = []
  | k == 0 = Bit False : bitsOf x n
  | otherwise = Bit True : bitsOf (x - k * m) n
  where
    n = s - 1
    m = 2 ^ n
    k = x `div` m
