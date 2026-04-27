export interface Designer {
  id: string
  name: string
}

export interface Look {
  id: string
  designer_id: string
  designer?: Designer
  season: string | null
  gender: string
  collection_type: string
  image_url: string
  description: string | null
}

export interface User {
  id: string
  username: string
  email: string
}
