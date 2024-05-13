module Art (export, Glyph, allGlyphs, Glyphs) where

import Codec.Picture
import Etc
import System.Directory (createDirectory)

glyphBits :: Int
glyphBits = 8

allGlyphs :: [Glyph]
allGlyphs = map byteToGlyph [0 .. 2 ^ glyphBits - 1]

newtype Glyph = Glyph (Bool, Bool, Bool, Bool, Bool, Bool, Bool, Bool)

newtype Glyphs = Glyphs [[Glyph]]

instance Show Glyph where
  show (Glyph (a0, a1, a2, a3, a4, a5, a6, a7)) =
    concatMap (show . Bit) [a0, a1, a2, a3, a4, a5, a6, a7]

instance Show Glyphs where
  show (Glyphs as) = dropBack 1 $ concatMap ((++ " ") . dropBack 1 . concatMap ((++ "+") . show)) as
    where
      dropBack i = reverse . drop i . reverse

instance Read Glyph where
  readsPrec _ as
    | all (\i -> i == '0' || i == '1') as = case map (== '1') as of
        [a0, a1, a2, a3, a4, a5, a6, a7] -> [(Glyph (a0, a1, a2, a3, a4, a5, a6, a7), "")]
        _ -> undefined
    | otherwise = undefined

instance Read Glyphs where
  readsPrec _ s = [(Glyphs (map (map read . lines . map (\i -> if i == '+' then '\n' else i)) $ lines $ map (\i -> if i == ' ' then '\n' else i) s), "")]

byteToGlyph :: Int -> Glyph
byteToGlyph a = case bitsOf a glyphBits of
  [Bit a0, Bit a1, Bit a2, Bit a3, Bit a4, Bit a5, Bit a6, Bit a7] -> Glyph (a0, a1, a2, a3, a4, a5, a6, a7)
  _ -> Glyph (True, True, True, True, True, True, True, True)

glyphsToBitmap :: Glyphs -> Matrix Bool
glyphsToBitmap (Glyphs as) = map (\x -> map (\y -> o (x, y)) [0 .. h * 12]) [0 .. w * 6]
  where
    (h, w) = matDims as
    o (x, y) =
      let (bX, bY) = (x `div` 6, y `div` 12)
          (lX, lY) = (x `mod` 6, y `mod` 12)
          f (blockX, blockY) (localX, localY) = (((blockX >= 0 && blockX < w) && (blockY >= 0 && blockY < h)) && (bitmaps !! blockY !! blockX !! localX !! localY))
       in f (bX, bY) (lX, lY)
            || ( (lX == 0 && (lY == 0 || lY == 6))
                   && (f (bX - 1, bY - 1) (6, 12) || f (bX, bY - 1) (lX, 12) || f (bX - 1, bY) (6, lY))
               )
    bitmaps = map (map glyphToBitmap) as
      where
        glyphToBitmap (Glyph (a0, a1, a2, a3, a4, a5, a6, a7)) = map (\x -> map (\y -> pixel (x, y)) [0 :: Int .. 12]) [0 .. 6]
          where
            pixel (x, y) =
              any
                (uncurry (&&))
                [ (a0, y == 6 + x),
                  (a1, x == 0 && y >= 6),
                  (a2, y >= 6 && y == 12 - x),
                  (a3, y == 6),
                  (a4, y == x),
                  (a5, x == 0 && y <= 6),
                  (a6, y <= 6 && y == 6 - x),
                  (a7, y == 0)
                ]

glyphToPaths :: Glyph -> (Double, Double) -> Double -> String
glyphToPaths a (px, py) scale =
  concatMap
    (\(b, i) -> if b then i else "")
    ( [ (b0, horizontal 0),
        (b1, diagonal False 0),
        (b2, vertical 0),
        (b3, diagonal True 0),
        (b4, horizontal 1),
        (b5, diagonal False 1),
        (b6, vertical 1),
        (b7, diagonal True 1),
        (b1 || b3, diamond 0),
        (b5 || b7, diamond 1),
        (b0 || b2 || b3, square (0, 0)),
        (b0 || b1, square (1, 0)),
        (b3 || b4 || b5, square (1, 1)),
        (b5 || b6, square (0, 2)),
        (b7, square (1, 2)),
        ((b4 || b6 || b7) || (b2 || b1), square (0, 1))
      ]
        ++ concatMap
          ( \(b, (f, y)) ->
              let (x0, x1) = if f then (6, 1) else (1, 6)
               in map
                    (b,)
                    [ triangle (False, f) (x0 - offset, y + 6),
                      triangle (True, not f) (x0 + offset, y + 6),
                      triangle (False, f) (x1 - offset, y + 1),
                      triangle (True, not f) (x1 + offset, y + 1)
                    ]
          )
          [ (b1, (False, 0)),
            (b3, (True, 0)),
            (b5, (False, 6)),
            (b7, (True, 6))
          ]
    )
  where
    Glyph (b7, b6, b5, b4, b3, b2, b1, b0) = a
    offset = sqrt 2 / 2
    center = 7 / 2
    triangle (fh, fv) (x, y) =
      polygon $
        map
          ((\(x0, y0) -> (x0 + x, y0 + y)) . (\(x0, y0) -> (if fh then -x0 else x0, if fv then -y0 else y0)))
          [(0, 0), (offset, -offset), (offset, 0)]
    square (x, y) =
      polygon $
        map
          (\(x0, y0) -> (x0 + x * 6, y0 + y * 6))
          [(0, 0), (1, 0), (1, 1), (0, 1)]
    diamond y =
      polygon $
        map
          (\(x0, y0) -> (center + x0, y * 6 + center + y0))
          [(-offset, 0), (0, -offset), (offset, 0), (0, offset)]
    diagonal f y =
      let m (x0, y0) = (if f then x0 else 7 - x0, y0 + y * 6)
       in polygon
            ( map
                m
                [ (1, 1),
                  (1 + offset, 1),
                  (center, center - offset),
                  (center - offset, center),
                  (1, 1 + offset)
                ]
            )
            ++ polygon
              ( map
                  (m . \(x0, y0) -> (x0 + 6, y0 + 6))
                  [ (0, 0),
                    (-offset, 0),
                    (-center + 1, -center + offset + 1),
                    (-center + offset + 1, -center + 1),
                    (0, -offset)
                  ]
              )
    vertical y =
      polygon
        [ (0, 1 + y * 6),
          (1, 1 + y * 6),
          (1, 1 + (y + 1) * 6 - 1),
          (0, 1 + (y + 1) * 6 - 1)
        ]
    horizontal y =
      polygon $
        map
          (\(x0, y0) -> (x0, y0 + y * 6))
          [(1, 0), (6, 0), (6, 1), (1, 1)]
    polygon :: [(Double, Double)] -> String
    polygon [] = ""
    polygon (xy0 : xys) = "<path d='" ++ concatMap (++ " ") (("M" ++ xy xy0) : map (("L" ++) . xy) xys) ++ "Z'/>"
      where
        xy (x, y) = show ((px * 6 + x) * scale) ++ " " ++ show ((py * 12 + y) * scale)

glyphsToSvg :: Glyphs -> String
glyphsToSvg (Glyphs as) = xmlWrap "svg" [("viewBox", "0 0 " ++ show ((fromIntegral width * 6) * scale) ++ " " ++ show ((fromIntegral height * 6 * 2) * scale))] $ concatMap (\(i, a) -> r (fromIntegral i) (reverse a)) (indexed as)
  where
    scale = 128
    (height, width) = matDims as
    r y (a : ar) = glyphToPaths a (fromIntegral $ length ar, y) scale ++ r y ar
    r _ [] = ""
    xmlWrap tag attributes body = "<" ++ tag ++ concatMap (\(a, b) -> " " ++ a ++ "=" ++ "\"" ++ b ++ "\"") attributes ++ ">" ++ body ++ "</" ++ tag ++ ">"

export :: Glyphs -> IO ()
export glyphs = do
  createDirectory path
  writeFile (path ++ "/.svg") svg
  saveBmpImage (path ++ "/.bmp") bmp
  savePngImage (path ++ "/.png") png
  where
    path = "./" ++ show glyphs
    bmp = png
    svg = glyphsToSvg glyphs
    png = ImageRGBA8 $ bitmapToPng $ glyphsToBitmap glyphs
      where
        bitmapToPng bitmap = uncurry (generateImage draw) (matDims bitmap)
          where
            draw x y
              | bitmap !! x !! y = PixelRGBA8 255 255 255 255
              | otherwise = PixelRGBA8 0 0 0 0
