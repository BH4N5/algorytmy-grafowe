-- Integration using 3-point Gauss-Legendre quadrature rule
gaussQuad :: Floating a => (a -> a) -> a -> a -> a
gaussQuad f a b = c * sum (zipWith (*) wi (map g xi))
  where
    c = (b - a) / 2
    xi = [-sqrt (3 / 5), 0, sqrt (3 / 5)]
    wi = [5 / 9, 8 / 9, 5 / 9]
    g = f . (\x -> (b - a) / 2 * x + (a + b) / 2)

-- Integral
integral :: (Enum a, Floating a) => (a -> a) -> a -> a -> a -> a
integral f a b n = sum [area i | i <- [1 .. n]]
  where
    area i = gaussQuad f (a + (i - 1) * dx) (a + i * dx)
      where
        dx = (b - a) / n

-- Some matrix prototyping

at :: [[a]] -> (Int, Int) -> a
at m (i, j) = (m !! i) !! j

nullMatrix :: Int -> Int -> [[Int]]
nullMatrix n m = [[0 | x <- [1 .. n]] | y <- [1 .. m]]

unitMatrix :: Int -> [[Int]]
unitMatrix n = [[if x == y then 1 else 0 | x <- [1 .. n]] | y <- [1 .. n]]

prettyMatrix :: Show a => [[a]] -> IO ()
prettyMatrix [] = putStr ""
prettyMatrix (x : xs) = do
  putStrLn $ concat $ zipWith (++) (map show x) ([" " | i <- [1 .. length x]] ++ [""])
  prettyMatrix xs

-- I think I'm gonna go with Julia lang for this project, but Haskell is a very
-- nice language :-)
