using LinearAlgebra, Plots

function gaussQuad(f, a, b)
    c = (b - a) / 2
    g = x -> (b - a) / 2 * x + (a + b) / 2
    nodes = [-sqrt(3 / 5), 0, sqrt(3 / 5)]
    weights = [5 / 9, 8 / 9, 5 / 9]
    return c * sum([weights[i] * f(g(nodes[i])) for i = 1:3])
end

# Integration using trapezoidal rule (uses Gauss-Legendre quadrature for every
# interval)
function integral(f, a, b, N)
    dx = (b - a) / N
    res = 0
    for i = 1:N
        res += gaussQuad(f, a + (i - 1) * dx, a + i * dx)
    end
    return res
end

# Solving an ODE d/dx (E(x) du/dx) = 0 for E(x) = ... and boundary conditions
# ... using Finitie Element Method (FEM)

function v(k, x, a, b, n)
    dx = (b - a) / n
    xk = a + k * dx
    if x <= xk && x >= xk - dx
        return 1 + (x - xk) / (dx)
    elseif x >= xk && x <= xk + dx
        return 1 + (xk - x) / (dx)
    else
        return 0
    end
end

function v1(k, x, a, b, n)
    dx = (b - a) / n
    xk = a + k * dx
    if x <= xk && x >= xk - dx
        return 1 / (dx)
    elseif x >= xk && x <= xk + dx
        return (-1) / (dx)
    else
        return 0
    end
end

# Naprawić te funkcje Lin({vk})

function FEM(n)
    f = x -> sin(x)
    a, b = 0, 2
    V = [x -> v(k, x, a, b, n) for k = 1:n-1]
    V1 = [x -> v1(k, x, a, b, n) for k = 1:n-1]

    B = [[float(0) for i = 1:n-1] for j = 1:n-1]
    for i = 1:n-1
        for j = 1:n-1
            I = integral(x -> V1[i](x) * V1[j](x), a, b, 10^4)
            B[i][j] = I
        end
    end
    B = hcat(B...)

    L = [float(0) for i = 1:n-1]
    for i = 1:n-1
        I = integral(x -> f(x) * V[i](x), a, b, 10^4)
        L[i] = -I
    end

    A = B \ L
    u = x -> sum([A[i] * V[i](x) for i = 1:n-1])

    return B, L, A, u
end


#B, L, A, u = FEM(20)

#print(u(1))
#x = range(0, 2, 10)
#plot(x, u.(x))

#print(u(1))
