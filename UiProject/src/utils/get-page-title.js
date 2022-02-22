import defaultSettings from '@/settings'

const title = defaultSettings.title || '质量实验室'

export default function getPageTitle(pageTitle) {
  if (pageTitle && pageTitle !== 'Dashboard') {
    return `${pageTitle} - ${title}`
  }
  return `${title}`
}
