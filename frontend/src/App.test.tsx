import { render, screen } from '@testing-library/react'
import { describe, it, expect, vi, beforeEach } from 'vitest'
import { App } from './App'

describe('App', () => {
    beforeEach(() => {
        vi.resetAllMocks()
    })

    it('отображает заголовок My Messenger', () => {
        vi.spyOn(globalThis, 'fetch').mockResolvedValue({
            json: () => Promise.resolve({ status: 'ok', version: '0.1.0' }),
        } as Response)

        render(<App />)
        expect(screen.getByText('My Messenger')).toBeInTheDocument()
    })

    it('показывает загрузку при старте', () => {
        vi.spyOn(globalThis, 'fetch').mockImplementation(
            () => new Promise(() => { })
        )

        render(<App />)
        expect(screen.getByText('Загрузка...')).toBeInTheDocument()
    })

    it('отображает статус API при успешном ответе', async () => {
        vi.spyOn(globalThis, 'fetch').mockResolvedValue({
            json: () => Promise.resolve({ status: 'ok', version: '0.1.0' }),
        } as Response)

        render(<App />)
        expect(await screen.findByText('ok')).toBeInTheDocument()
        expect(await screen.findByText('0.1.0')).toBeInTheDocument()
    })
})
