module Tal (translate, transcribe) where

import Data.Char (toLower)

alphabet :: [Char]
alphabet =
  ['ь', 'а', 'б', 'д', 'ф', 'э', 'ш', 'ж', 'х', 'н', 'ы', 'г', 'к', 'л', 'м', 'о', 'п', 'р', 'с', 'т', 'у', 'в', 'з']

shorten :: String -> String
shorten a = a
  where
    b =
      [ ("ьa", 'я'),
        ("тс", 'ц'),
        ("ьэ", 'е')
      ]

dict :: String -> String
dict "hello" = "салв'э"
dict _ = "~"

transcribe :: String -> String
transcribe a = shorten $ map toLower a

translate :: String -> String
translate a = unwords . map (shorten . dict) . words $ map toLower a
