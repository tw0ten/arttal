module Main where

import Art qualified
import System.Environment (getArgs)
import Tal qualified (transcribe, translate)

main :: IO ()
main = getArgs >>= parse
  where
    parse ("tal" : "ts" : str) = putStrLn $ Tal.transcribe (unwords str)
    parse ("tal" : "tl" : str) = putStrLn $ Tal.translate (unwords str)
    parse ("art" : glyphs) = Art.export . read $ unwords glyphs
    parse _ = putStrLn "arttal\n\ttal (ts|tl) <str?>\n\tart <glyphs?>"
