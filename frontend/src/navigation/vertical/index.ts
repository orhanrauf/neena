import build from './build'
import execute from './execute'
import train from './train'
import type { VerticalNavItems } from '@layouts/types'

export default [...build, ...execute, ...train] as VerticalNavItems
